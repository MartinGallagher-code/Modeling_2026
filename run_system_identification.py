#!/usr/bin/env python3
"""
Run System Identification for Modeling_2026
=============================================

Batch runner that loads each processor model, reads its measured CPI data,
and runs scipy.optimize.least_squares to fit correction terms that minimize
CPI prediction error.

Usage:
    python run_system_identification.py                    # all models
    python run_system_identification.py --family zilog     # one family
    python run_system_identification.py --processor z80    # one processor
    python run_system_identification.py --dry-run          # preview only
    python run_system_identification.py --verbose          # detailed output

Author: Grey-Box Performance Modeling Research
Date: January 2026
"""

import argparse
import importlib.util
import json
import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Ensure repo root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from common.system_identification import (
    IdentificationResult,
    identify_model,
    load_measurements_for_model,
)
from common.base_model import get_model_parameters


# ---------------------------------------------------------------------------
# Model loading (same pattern as run_accuracy_tests.py)
# ---------------------------------------------------------------------------

def load_model(model_path: Path) -> Tuple[Any, Optional[str]]:
    """Dynamically load a processor model from its _validated.py file.

    Returns:
        (model_instance, None) on success, or (None, error_message) on failure.
    """
    try:
        spec = importlib.util.spec_from_file_location("model", model_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for name in dir(module):
            if name.endswith("Model") and name != "BaseProcessorModel":
                obj = getattr(module, name)
                if isinstance(obj, type):
                    return obj(), None

        return None, "No Model class found"
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

def discover_processors(
    repo_root: Path,
    family_filter: Optional[str] = None,
    processor_filter: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Discover processors from index.json.

    Returns list of dicts with keys: family, processor, model_dir, model_file.
    """
    index_path = repo_root / "index.json"
    if not index_path.exists():
        print(f"ERROR: {index_path} not found")
        return []

    with open(index_path) as f:
        index = json.load(f)

    processors = []
    for family, info in index.get("families", {}).items():
        if family_filter and family != family_filter:
            continue
        for proc in info.get("processors", []):
            if processor_filter and proc != processor_filter:
                continue

            model_dir = repo_root / "models" / family / proc
            if not model_dir.exists():
                continue

            # Find the validated model file
            current_dir = model_dir / "current"
            if not current_dir.exists():
                continue
            model_files = list(current_dir.glob("*_validated.py"))
            if not model_files:
                continue

            processors.append({
                "family": family,
                "processor": proc,
                "model_dir": model_dir,
                "model_file": model_files[0],
            })

    return processors


# ---------------------------------------------------------------------------
# Result saving
# ---------------------------------------------------------------------------

def save_identification_result(
    model_dir: Path,
    proc_name: str,
    result: IdentificationResult,
    dry_run: bool = False,
) -> None:
    """Save identification results to the processor's validation directory."""
    if dry_run:
        return

    # Save corrections to a dedicated JSON file
    output_dir = model_dir / "identification"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "sysid_result.json"

    data = {
        "processor": proc_name,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "converged": result.converged,
        "iterations": result.iterations,
        "loss_before": round(result.loss_before, 6),
        "loss_after": round(result.loss_after, 6),
        "cpi_error_percent": round(result.cpi_error_percent, 2),
        "message": result.message,
        "corrections": {k: round(v, 6) for k, v in result.corrections.items()},
        "residuals_before": {k: round(v, 4) for k, v in result.residuals_before.items()},
        "residuals_after": {k: round(v, 4) for k, v in result.residuals_after.items()},
        "free_parameters": result.free_parameters,
    }

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    # Also update validation JSON if it exists
    val_dir = model_dir / "validation"
    val_files = list(val_dir.glob("*_validation.json")) if val_dir.exists() else []
    if val_files:
        try:
            with open(val_files[0]) as f:
                val_data = json.load(f)

            if "accuracy" not in val_data:
                val_data["accuracy"] = {}
            val_data["accuracy"]["sysid_loss_before"] = round(result.loss_before, 6)
            val_data["accuracy"]["sysid_loss_after"] = round(result.loss_after, 6)
            val_data["accuracy"]["sysid_cpi_error_percent"] = round(result.cpi_error_percent, 2)
            val_data["accuracy"]["sysid_converged"] = result.converged
            val_data["accuracy"]["sysid_date"] = datetime.now().strftime("%Y-%m-%d")

            with open(val_files[0], "w") as f:
                json.dump(val_data, f, indent=2)
        except Exception:
            pass  # non-critical


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

def run_identification(
    repo_root: Path,
    family_filter: Optional[str] = None,
    processor_filter: Optional[str] = None,
    dry_run: bool = False,
    verbose: bool = False,
) -> List[Dict[str, Any]]:
    """Run system identification across all matching processors.

    Returns a list of summary dicts for the results table.
    """
    processors = discover_processors(repo_root, family_filter, processor_filter)
    if not processors:
        print("No processors found matching filters.")
        return []

    print(f"Found {len(processors)} processor(s) to identify.\n")

    summaries = []
    skipped_no_measurements = 0
    skipped_load_error = 0
    skipped_no_params = 0
    errors = 0

    for entry in processors:
        family = entry["family"]
        proc = entry["processor"]
        model_dir = entry["model_dir"]
        model_file = entry["model_file"]
        label = f"{family}/{proc}"

        # Load measurements
        measurements = load_measurements_for_model(model_dir)
        if not measurements:
            skipped_no_measurements += 1
            if verbose:
                print(f"  SKIP  {label:35s} — no measured_cpi.json")
            continue

        # Load model
        model, load_err = load_model(model_file)
        if model is None:
            skipped_load_error += 1
            if verbose:
                print(f"  ERROR {label:35s} — {load_err}")
            continue

        # Check that model has parameters
        params = get_model_parameters(model)
        if not params:
            skipped_no_params += 1
            if verbose:
                print(f"  SKIP  {label:35s} — no parameters")
            continue

        # Run identification
        try:
            result = identify_model(model, measurements, verbose=2 if verbose else 0)
        except Exception as e:
            errors += 1
            if verbose:
                print(f"  FAIL  {label:35s} — {type(e).__name__}: {e}")
                traceback.print_exc()
            summaries.append({
                "processor": label,
                "error_before": None,
                "error_after": None,
                "converged": False,
                "status": "ERROR",
                "message": str(e),
            })
            continue

        # Compute error-before for summary
        error_before_pct = _compute_typical_error(
            result.residuals_before, measurements
        )
        error_after_pct = result.cpi_error_percent

        status = "OK" if result.converged else "NO_CONV"
        if error_after_pct < 5.0:
            status_display = "PASS"
        elif error_after_pct < 15.0:
            status_display = "MARGINAL"
        else:
            status_display = "FAIL"

        summary = {
            "processor": label,
            "error_before": round(error_before_pct, 2),
            "error_after": round(error_after_pct, 2),
            "converged": result.converged,
            "status": status_display,
            "iterations": result.iterations,
            "n_free": len(result.free_parameters),
        }
        summaries.append(summary)

        # Print progress
        conv_str = "Y" if result.converged else "N"
        print(
            f"  {status_display:8s} {label:35s}  "
            f"err: {error_before_pct:6.2f}% -> {error_after_pct:6.2f}%  "
            f"conv={conv_str}  iter={result.iterations}  "
            f"free={len(result.free_parameters)}"
        )

        # Save results
        save_identification_result(model_dir, proc, result, dry_run)

    # Print skip summary
    print()
    if skipped_no_measurements:
        print(f"Skipped (no measurements): {skipped_no_measurements}")
    if skipped_load_error:
        print(f"Skipped (load error):      {skipped_load_error}")
    if skipped_no_params:
        print(f"Skipped (no parameters):   {skipped_no_params}")
    if errors:
        print(f"Errors during optimization: {errors}")

    return summaries


def _compute_typical_error(
    residuals: Dict[str, float], measurements: Dict[str, float]
) -> float:
    """Compute % error on the 'typical' workload (or first available)."""
    for workload in ["typical"] + sorted(residuals.keys()):
        if workload in residuals and workload in measurements:
            measured = measurements[workload]
            if measured > 0:
                return abs(residuals[workload]) / measured * 100.0
    return float("inf")


# ---------------------------------------------------------------------------
# Summary table
# ---------------------------------------------------------------------------

def print_summary(summaries: List[Dict[str, Any]]) -> None:
    """Print a formatted summary table."""
    if not summaries:
        return

    print()
    print("=" * 85)
    print("SYSTEM IDENTIFICATION SUMMARY")
    print("=" * 85)
    print(
        f"  {'Processor':35s}  {'Before':>8s}  {'After':>8s}  "
        f"{'Conv':>4s}  {'Status':>8s}"
    )
    print("-" * 85)

    passed = marginal = failed = err = 0
    for s in sorted(summaries, key=lambda x: x["processor"]):
        eb = f"{s['error_before']:.2f}%" if s["error_before"] is not None else "N/A"
        ea = f"{s['error_after']:.2f}%" if s["error_after"] is not None else "N/A"
        conv = "Y" if s.get("converged") else "N"
        status = s.get("status", "?")
        print(f"  {s['processor']:35s}  {eb:>8s}  {ea:>8s}  {conv:>4s}  {status:>8s}")

        if status == "PASS":
            passed += 1
        elif status == "MARGINAL":
            marginal += 1
        elif status == "FAIL":
            failed += 1
        else:
            err += 1

    print("-" * 85)
    total = len(summaries)
    print(
        f"  Total: {total}  |  PASS (<5%): {passed}  |  "
        f"MARGINAL (5-15%): {marginal}  |  FAIL (>15%): {failed}  |  "
        f"ERROR: {err}"
    )
    print("=" * 85)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Run system identification on processor models"
    )
    parser.add_argument(
        "--family",
        help="Only process models in this family (e.g. 'zilog', 'intel')",
    )
    parser.add_argument(
        "--processor",
        help="Only process this specific processor (e.g. 'z80')",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview only — don't write result files",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output including skipped models",
    )

    args = parser.parse_args()

    print("=" * 85)
    print("SYSTEM IDENTIFICATION — Modeling_2026")
    print("=" * 85)
    print(f"Repository: {REPO_ROOT}")
    if args.family:
        print(f"Family filter: {args.family}")
    if args.processor:
        print(f"Processor filter: {args.processor}")
    print(f"Mode: {'DRY-RUN' if args.dry_run else 'WRITE RESULTS'}")
    print()

    summaries = run_identification(
        REPO_ROOT,
        family_filter=args.family,
        processor_filter=args.processor,
        dry_run=args.dry_run,
        verbose=args.verbose,
    )

    print_summary(summaries)

    if args.dry_run:
        print("\nDRY RUN — no files were written.")


if __name__ == "__main__":
    main()
