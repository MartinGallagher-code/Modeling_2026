#!/usr/bin/env python3
"""
Apply External Benchmark Data to Processor Models
====================================================

Reads external benchmark data from external_validation/benchmark_data.json,
converts to per-workload CPI values, updates measured_cpi.json files,
optionally re-runs system identification and applies new corrections.

Usage:
    python tools/apply_external_benchmarks.py                    # all processors
    python tools/apply_external_benchmarks.py --processor i8088  # one processor
    python tools/apply_external_benchmarks.py --dry-run          # preview only
    python tools/apply_external_benchmarks.py --skip-sysid       # skip re-identification
    python tools/apply_external_benchmarks.py --update-remaining # mark non-benchmark sources

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

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.benchmark_to_cpi import (
    dmips_to_cpi,
    mips_to_cpi,
    spec_to_estimated_cpi,
    peak_mips_to_cpi,
    derive_workload_cpis,
    compute_uncertainty,
    compute_confidence,
)


# ---------------------------------------------------------------------------
# Load benchmark database
# ---------------------------------------------------------------------------

def load_benchmark_database(repo_root: Path) -> Dict[str, List[Dict]]:
    """Load external benchmark data, grouped by processor name.

    Returns dict mapping processor name -> list of benchmark entries.
    """
    path = repo_root / "external_validation" / "benchmark_data.json"
    if not path.exists():
        print(f"ERROR: {path} not found")
        return {}

    with open(path) as f:
        data = json.load(f)

    # Group by processor
    by_processor = {}
    for entry in data.get("benchmarks", []):
        proc = entry["processor"]
        by_processor.setdefault(proc, []).append(entry)

    return by_processor


def select_best_benchmark(entries: List[Dict], data_width: int = 32) -> Dict:
    """Select the most reliable benchmark entry for a processor.

    For 8-bit processors, prefer MIPS ratings over Dhrystone because
    Dhrystone is a poor benchmark for 8-bit architectures (it requires
    many multi-byte operations that inflate CPI unrealistically).

    For 16+ bit processors, Dhrystone is the most reliable standardized
    benchmark for CPI derivation.
    """
    if data_width <= 8:
        # For 8-bit processors, prefer native MIPS ratings
        priority = {
            "mips_rating": 1,
            "published_mips": 1,
            "arm_benchmark": 2,
            "specint89": 3,
            "specint92": 3,
            "dhrystone": 4,  # Demoted for 8-bit
            "dsp_peak": 5,
            "datasheet_peak": 6,
        }
    else:
        priority = {
            "dhrystone": 1,
            "specint92": 2,
            "specint89": 3,
            "arm_benchmark": 4,
            "published_mips": 5,
            "mips_rating": 5,
            "dsp_peak": 6,
            "datasheet_peak": 7,
        }
    return min(entries, key=lambda e: priority.get(e.get("benchmark_type", ""), 99))


def compute_base_cpi(entry: Dict) -> float:
    """Compute baseline CPI from a benchmark entry."""
    btype = entry["benchmark_type"]
    clock = entry["clock_mhz"]
    raw = entry["raw_value"]

    if btype == "dhrystone":
        return dmips_to_cpi(clock, raw)
    elif btype in ("mips_rating", "published_mips", "arm_benchmark"):
        return mips_to_cpi(clock, raw)
    elif btype in ("specint89", "specint92", "specfp92"):
        return spec_to_estimated_cpi(clock, raw, btype)
    elif btype == "dsp_peak":
        # DSP peak MIPS/MFLOPS - use 60% utilization
        return peak_mips_to_cpi(clock, raw, utilization=0.6)
    elif btype == "datasheet_peak":
        return peak_mips_to_cpi(clock, raw, utilization=0.5)
    else:
        return mips_to_cpi(clock, raw)


# ---------------------------------------------------------------------------
# Update measured_cpi.json
# ---------------------------------------------------------------------------

def load_existing_measured_cpi(model_dir: Path) -> Optional[Dict]:
    """Load existing measured_cpi.json."""
    path = model_dir / "measurements" / "measured_cpi.json"
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def get_existing_workloads(existing: Dict) -> List[str]:
    """Get list of workload names from existing measured_cpi.json."""
    measurements = existing.get("measurements", [])
    return [m["workload"] for m in measurements if "workload" in m]


def get_model_workloads(model_dir: Path) -> List[str]:
    """Try to read the model's workload profile names."""
    current_dir = model_dir / "current"
    if not current_dir.exists():
        return []
    model_files = list(current_dir.glob("*_validated.py"))
    if not model_files:
        return []
    try:
        spec = importlib.util.spec_from_file_location("model", model_files[0])
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for name in dir(module):
            if name.endswith("Model") and name != "BaseProcessorModel":
                obj = getattr(module, name)
                if isinstance(obj, type):
                    instance = obj()
                    profiles = getattr(instance, 'workload_profiles', {})
                    return list(profiles.keys())
    except Exception:
        pass
    return []


def get_model_data_width(model_dir: Path) -> int:
    """Try to read the model's data_width from its _validated.py file."""
    current_dir = model_dir / "current"
    if not current_dir.exists():
        return 32
    model_files = list(current_dir.glob("*_validated.py"))
    if not model_files:
        return 32
    try:
        spec = importlib.util.spec_from_file_location("model", model_files[0])
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for name in dir(module):
            if name.endswith("Model") and name != "BaseProcessorModel":
                obj = getattr(module, name)
                if isinstance(obj, type):
                    instance = obj()
                    return getattr(instance, 'data_width', 32) or 32
    except Exception:
        pass
    return 32


def get_model_clock(model_dir: Path) -> Optional[float]:
    """Try to read the model's clock_mhz from its _validated.py file."""
    current_dir = model_dir / "current"
    if not current_dir.exists():
        return None
    model_files = list(current_dir.glob("*_validated.py"))
    if not model_files:
        return None
    try:
        spec = importlib.util.spec_from_file_location("model", model_files[0])
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for name in dir(module):
            if name.endswith("Model") and name != "BaseProcessorModel":
                obj = getattr(module, name)
                if isinstance(obj, type):
                    instance = obj()
                    return getattr(instance, 'clock_mhz', None)
    except Exception:
        pass
    return None


def get_model_year(model_dir: Path) -> int:
    """Try to read the model's year from its _validated.py file."""
    current_dir = model_dir / "current"
    if not current_dir.exists():
        return 1980
    model_files = list(current_dir.glob("*_validated.py"))
    if not model_files:
        return 1980
    try:
        spec = importlib.util.spec_from_file_location("model", model_files[0])
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for name in dir(module):
            if name.endswith("Model") and name != "BaseProcessorModel":
                obj = getattr(module, name)
                if isinstance(obj, type):
                    instance = obj()
                    return getattr(instance, 'year', 1980) or 1980
    except Exception:
        pass
    return 1980


def update_measured_cpi(
    model_dir: Path,
    processor: str,
    benchmark_entry: Dict,
    base_cpi: float,
    dry_run: bool = False,
) -> Tuple[bool, str]:
    """Update measured_cpi.json with benchmark-derived CPI values.

    Preserves existing file structure, updates CPI values and source info.
    """
    path = model_dir / "measurements" / "measured_cpi.json"

    existing = load_existing_measured_cpi(model_dir)
    if existing is None:
        return False, "no existing measured_cpi.json"

    # Determine workloads: use existing file's workloads, but also add any
    # model workloads that are missing from the measurement file
    existing_workloads = get_existing_workloads(existing)
    model_workloads = get_model_workloads(model_dir)
    all_workloads = list(dict.fromkeys(existing_workloads + model_workloads))  # preserve order, dedupe
    if not all_workloads:
        return False, "no workloads in existing file or model"

    # Get model year for era-appropriate adjustment factors
    year = get_model_year(model_dir)

    # Derive per-workload CPI values
    workload_cpis = derive_workload_cpis(base_cpi, year=year, workloads=all_workloads)

    # Compute uncertainty and confidence
    btype = benchmark_entry["benchmark_type"]
    uncertainty = compute_uncertainty(btype, base_cpi)
    confidence = compute_confidence(btype)

    # Build source detail string
    source_detail = benchmark_entry.get("source_detail", "")
    source_url = ""
    sources_db = None
    try:
        with open(REPO_ROOT / "external_validation" / "benchmark_data.json") as f:
            sources_db = json.load(f).get("sources", {})
    except Exception:
        pass
    if sources_db:
        src_key = benchmark_entry.get("source_key", "")
        if src_key in sources_db:
            source_url = sources_db[src_key].get("url", "")

    # Build common fields for new/updated measurements
    notes_str = (
        f"Derived from {btype}: {benchmark_entry['raw_value']} "
        f"{benchmark_entry.get('unit', '')} @ {benchmark_entry['clock_mhz']}MHz. "
        f"Original: {benchmark_entry.get('notes', '')}"
    )

    # Update each existing measurement
    updated_workloads = set()
    for m in existing.get("measurements", []):
        workload = m.get("workload")
        if workload in workload_cpis:
            m["measured_cpi"] = workload_cpis[workload]
            m["source"] = "published_benchmark"
            m["source_detail"] = source_detail
            if source_url:
                m["source_url"] = source_url
            m["uncertainty"] = uncertainty
            m["confidence"] = confidence
            m["date_measured"] = datetime.now().strftime("%Y-%m-%d")
            m["notes"] = notes_str
            if "conditions" not in m or m["conditions"] is None:
                m["conditions"] = {}
            updated_workloads.add(workload)

    # Add missing workloads that exist in the model but not in the file
    for workload, cpi_val in workload_cpis.items():
        if workload not in updated_workloads:
            existing.setdefault("measurements", []).append({
                "workload": workload,
                "measured_cpi": cpi_val,
                "source": "published_benchmark",
                "source_detail": source_detail,
                "source_url": source_url,
                "conditions": {},
                "uncertainty": uncertainty,
                "confidence": confidence,
                "date_measured": datetime.now().strftime("%Y-%m-%d"),
                "notes": notes_str,
            })

    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(existing, f, indent=2)

    return True, f"updated {len(workload_cpis)} workloads, base_cpi={base_cpi:.3f}"


# ---------------------------------------------------------------------------
# System identification re-run
# ---------------------------------------------------------------------------

def run_sysid_for_model(model_dir: Path, proc_name: str, dry_run: bool = False) -> Optional[Dict]:
    """Re-run system identification for a single processor model."""
    try:
        from common.system_identification import identify_model, load_measurements_for_model
        from common.base_model import get_model_parameters

        # Load measurements
        measurements = load_measurements_for_model(model_dir)
        if not measurements:
            return None

        # Load model
        current_dir = model_dir / "current"
        model_files = list(current_dir.glob("*_validated.py"))
        if not model_files:
            return None

        spec = importlib.util.spec_from_file_location("model", model_files[0])
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        model = None
        for name in dir(module):
            if name.endswith("Model") and name != "BaseProcessorModel":
                obj = getattr(module, name)
                if isinstance(obj, type):
                    model = obj()
                    break

        if model is None:
            return None

        # Zero out existing corrections before re-identification
        if hasattr(model, 'corrections'):
            for key in model.corrections:
                model.corrections[key] = 0.0

        # Run identification
        result = identify_model(model, measurements)

        if not dry_run:
            # Save sysid result
            output_dir = model_dir / "identification"
            output_dir.mkdir(parents=True, exist_ok=True)
            sysid_data = {
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
            with open(output_dir / "sysid_result.json", "w") as f:
                json.dump(sysid_data, f, indent=2)

        return {
            "converged": result.converged,
            "cpi_error_percent": result.cpi_error_percent,
            "corrections": result.corrections,
            "iterations": result.iterations,
        }
    except Exception as e:
        return {"error": str(e)}


def apply_corrections_to_model(model_dir: Path, corrections: Dict[str, float], dry_run: bool = False) -> bool:
    """Apply new correction values to the model source file."""
    current_dir = model_dir / "current"
    model_files = list(current_dir.glob("*_validated.py"))
    if not model_files:
        return False

    import re
    model_file = model_files[0]
    source = model_file.read_text()

    # Strip 'cor.' prefix from keys
    cor_values = {}
    for key, val in corrections.items():
        cat_name = key.replace("cor.", "") if key.startswith("cor.") else key
        cor_values[cat_name] = val

    if all(abs(v) < 1e-8 for v in cor_values.values()):
        return False

    # Build replacement
    items = []
    for cat, val in sorted(cor_values.items()):
        items.append(f"'{cat}': {val:.6f}")
    new_dict = "{\n" + ",\n".join(f"            {item}" for item in items) + "\n        }"
    new_line = f"self.corrections = {new_dict}"

    # Pattern 1: dict comprehension
    pattern1 = re.compile(
        r"self\.corrections\s*=\s*\{cat:\s*0\.0\s+for\s+cat\s+in\s+self\.\w+\}"
    )
    # Pattern 2: explicit dict (single-line or multi-line)
    pattern2 = re.compile(
        r"self\.corrections\s*=\s*\{[^}]*\}", re.DOTALL
    )

    if pattern1.search(source):
        new_source = pattern1.sub(new_line, source, count=1)
    elif pattern2.search(source):
        new_source = pattern2.sub(new_line, source, count=1)
    else:
        return False

    if new_source == source:
        return False

    if not dry_run:
        model_file.write_text(new_source)

    return True


# ---------------------------------------------------------------------------
# Update remaining processors (no external data)
# ---------------------------------------------------------------------------

def update_remaining_sources(repo_root: Path, processors_with_data: set, dry_run: bool = False) -> int:
    """Update source field for processors without external benchmark data.

    Changes source from 'emulator' to 'estimated' for honesty.
    """
    index_path = repo_root / "index.json"
    with open(index_path) as f:
        index = json.load(f)

    updated = 0
    for family, info in index.get("families", {}).items():
        for proc in info.get("processors", []):
            if proc in processors_with_data:
                continue

            model_dir = repo_root / "models" / family / proc
            path = model_dir / "measurements" / "measured_cpi.json"
            if not path.exists():
                continue

            try:
                with open(path) as f:
                    data = json.load(f)
            except Exception:
                continue

            changed = False
            for m in data.get("measurements", []):
                if m.get("source") == "emulator":
                    m["source"] = "estimated"
                    m["source_detail"] = "Estimated from architectural analysis and instruction timing"
                    if m.get("confidence") == "high":
                        m["confidence"] = "medium"
                    changed = True

            if changed and not dry_run:
                with open(path, "w") as f:
                    json.dump(data, f, indent=2)
                updated += 1
            elif changed:
                updated += 1

    return updated


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Apply external benchmark data to processor models"
    )
    parser.add_argument("--processor", help="Only process this processor")
    parser.add_argument("--family", help="Only process this family")
    parser.add_argument("--dry-run", action="store_true", help="Preview only")
    parser.add_argument("--skip-sysid", action="store_true", help="Skip system identification")
    parser.add_argument("--skip-corrections", action="store_true", help="Skip applying corrections")
    parser.add_argument("--update-remaining", action="store_true",
                       help="Also update source fields for processors without external data")
    parser.add_argument("--verbose", "-v", action="store_true")

    args = parser.parse_args()

    print("=" * 85)
    print("APPLY EXTERNAL BENCHMARK DATA")
    print("=" * 85)
    print(f"Mode: {'DRY-RUN' if args.dry_run else 'WRITE FILES'}")
    print()

    # Load benchmark database
    benchmark_db = load_benchmark_database(REPO_ROOT)
    print(f"Loaded benchmark data for {len(benchmark_db)} processors")

    # Load index
    index_path = REPO_ROOT / "index.json"
    with open(index_path) as f:
        index = json.load(f)

    # Build processor -> (family, model_dir) mapping
    proc_info = {}
    for family, info in index.get("families", {}).items():
        for proc in info.get("processors", []):
            model_dir = REPO_ROOT / "models" / family / proc
            if model_dir.exists():
                proc_info[proc] = {"family": family, "model_dir": model_dir}

    # Process each processor with benchmark data
    updated = 0
    sysid_run = 0
    corrections_applied = 0
    errors = 0
    processors_with_data = set()

    for proc_name, entries in sorted(benchmark_db.items()):
        if args.processor and proc_name != args.processor:
            continue
        if args.family and proc_info.get(proc_name, {}).get("family") != args.family:
            continue

        if proc_name not in proc_info:
            if args.verbose:
                print(f"  SKIP  {proc_name:35s} — not in index.json")
            continue

        info = proc_info[proc_name]
        model_dir = info["model_dir"]
        family = info["family"]
        label = f"{family}/{proc_name}"

        # Select best benchmark (considering processor data width)
        data_width = get_model_data_width(model_dir)
        best = select_best_benchmark(entries, data_width=data_width)

        # Compute base CPI
        try:
            base_cpi = compute_base_cpi(best)
        except Exception as e:
            print(f"  ERROR {label:35s} — CPI conversion: {e}")
            errors += 1
            continue

        # Sanity check CPI
        if base_cpi < 0.3 or base_cpi > 200:
            print(f"  WARN  {label:35s} — CPI={base_cpi:.2f} out of expected range [0.3, 200]")

        # Update measured_cpi.json
        success, msg = update_measured_cpi(model_dir, proc_name, best, base_cpi, args.dry_run)
        if success:
            updated += 1
            processors_with_data.add(proc_name)
            action = "WOULD" if args.dry_run else "UPDATE"
            print(f"  {action:7s} {label:35s} — {best['benchmark_type']:15s} CPI={base_cpi:7.2f}  ({msg})")
        else:
            if args.verbose:
                print(f"  SKIP  {label:35s} — {msg}")
            continue

        # Re-run system identification
        if not args.skip_sysid:
            sysid_result = run_sysid_for_model(model_dir, proc_name, args.dry_run)
            if sysid_result and "error" not in sysid_result:
                sysid_run += 1
                err_pct = sysid_result["cpi_error_percent"]
                conv = "Y" if sysid_result["converged"] else "N"
                if args.verbose:
                    print(f"          sysid: err={err_pct:.2f}% conv={conv} iter={sysid_result['iterations']}")

                # Apply corrections to source file
                if not args.skip_corrections and sysid_result.get("corrections"):
                    applied = apply_corrections_to_model(
                        model_dir, sysid_result["corrections"], args.dry_run
                    )
                    if applied:
                        corrections_applied += 1
            elif sysid_result and "error" in sysid_result:
                if args.verbose:
                    print(f"          sysid ERROR: {sysid_result['error']}")

    # Update remaining processors
    remaining_updated = 0
    if args.update_remaining:
        print()
        print("Updating source fields for remaining processors...")
        remaining_updated = update_remaining_sources(REPO_ROOT, processors_with_data, args.dry_run)
        print(f"  Updated {remaining_updated} processor(s) from 'emulator' to 'estimated'")

    # Summary
    print()
    print("=" * 85)
    print("SUMMARY")
    print("=" * 85)
    print(f"  Benchmark data available:    {len(benchmark_db)} processors")
    print(f"  measured_cpi.json updated:   {updated}")
    print(f"  System identification run:   {sysid_run}")
    print(f"  Corrections applied:         {corrections_applied}")
    print(f"  Errors:                      {errors}")
    if args.update_remaining:
        print(f"  Remaining sources updated:   {remaining_updated}")
    print("=" * 85)

    if args.dry_run:
        print("\nDRY RUN — no files were modified.")


if __name__ == "__main__":
    main()
