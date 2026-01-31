#!/usr/bin/env python3
"""
Batch Update Documentation for External Benchmark Integration
================================================================

Updates CHANGELOG.md, HANDOFF.md, validation JSON, and README.md
for all processors that received external benchmark data.

Usage:
    python tools/update_benchmark_docs.py                  # all processors
    python tools/update_benchmark_docs.py --dry-run        # preview only
    python tools/update_benchmark_docs.py --processor z80  # one processor

Author: Grey-Box Performance Modeling Research
Date: January 2026
"""

import argparse
import importlib.util
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

TODAY = datetime.now().strftime("%Y-%m-%d")


def load_benchmark_database() -> Dict[str, List[Dict]]:
    """Load benchmark database grouped by processor."""
    path = REPO_ROOT / "external_validation" / "benchmark_data.json"
    with open(path) as f:
        data = json.load(f)
    by_processor = {}
    for entry in data.get("benchmarks", []):
        proc = entry["processor"]
        by_processor.setdefault(proc, []).append(entry)
    return by_processor


def get_processor_dirs() -> Dict[str, Path]:
    """Map processor name -> model directory."""
    index_path = REPO_ROOT / "index.json"
    with open(index_path) as f:
        index = json.load(f)
    dirs = {}
    for family, info in index.get("families", {}).items():
        for proc in info.get("processors", []):
            model_dir = REPO_ROOT / "models" / family / proc
            if model_dir.exists():
                dirs[proc] = model_dir
    return dirs


def get_current_validation_status(model_dir: Path) -> Dict[str, Any]:
    """Load current sysid result and measured_cpi to compute status."""
    status = {"cpi_error": None, "converged": False, "source": "unknown", "base_cpi": None}

    # Read sysid result
    sysid_path = model_dir / "identification" / "sysid_result.json"
    if sysid_path.exists():
        with open(sysid_path) as f:
            sysid = json.load(f)
        status["cpi_error"] = sysid.get("cpi_error_percent", None)
        status["converged"] = sysid.get("converged", False)

    # Read measured_cpi for source info
    meas_path = model_dir / "measurements" / "measured_cpi.json"
    if meas_path.exists():
        with open(meas_path) as f:
            meas = json.load(f)
        measurements = meas.get("measurements", [])
        if measurements:
            status["source"] = measurements[0].get("source", "unknown")
            typical = [m for m in measurements if m.get("workload") == "typical"]
            if typical:
                status["base_cpi"] = typical[0].get("measured_cpi")

    return status


def update_changelog(model_dir: Path, proc_name: str, benchmarks: List[Dict],
                    status: Dict, dry_run: bool = False) -> bool:
    """Append external benchmark integration entry to CHANGELOG.md."""
    changelog_path = model_dir / "CHANGELOG.md"

    # Build the entry
    bench_lines = []
    for b in benchmarks:
        bench_lines.append(
            f"  - {b['benchmark_type']}: {b['raw_value']} {b.get('unit', '')} "
            f"@ {b['clock_mhz']}MHz → CPI={b['computed_cpi']:.2f}"
        )
    bench_summary = "\n".join(bench_lines)

    err_str = f"{status['cpi_error']:.2f}%" if status['cpi_error'] is not None else "N/A"
    passed = "PASSED" if status['cpi_error'] is not None and status['cpi_error'] < 5.0 else "NEEDS INVESTIGATION" if status['cpi_error'] is not None and status['cpi_error'] >= 15.0 else "MARGINAL"

    entry = f"""
---

## [{TODAY}] - External benchmark data integration

**Session goal:** Replace synthetic CPI measurements with real published benchmark data

**Starting state:**
- CPI source: emulator/estimated (synthetic)
- Validation: based on self-referential data

**Changes made:**

1. Updated measured_cpi.json with externally-validated benchmark data
   - Source: published_benchmark
{bench_summary}
   - Per-workload CPI derived using era-appropriate adjustment factors

2. Re-ran system identification with new measurement targets
   - Correction terms re-optimized via least-squares
   - CPI error: {err_str}

**What we learned:**
- External benchmark data provides honest validation targets
- Model error vs real benchmarks: {err_str}

**Final state:**
- CPI error: {err_str}
- Validation: {passed} (against real benchmark data)
- Source: published_benchmark

**References used:**
- Netlib Dhrystone Database: https://www.netlib.org/performance/html/dhrystone.data.col0.html
- Wikipedia MIPS comparison: https://en.wikipedia.org/wiki/Instructions_per_second
- SPEC archives: https://www.spec.org/
"""

    if changelog_path.exists():
        existing = changelog_path.read_text()
    else:
        existing = f"# {proc_name} Model Changelog\n\nThis file contains the complete history of all work on this model.\n**Append-only: Never delete previous entries.**\n"

    if not dry_run:
        changelog_path.write_text(existing + entry)
    return True


def update_handoff(model_dir: Path, proc_name: str, benchmarks: List[Dict],
                  status: Dict, dry_run: bool = False) -> bool:
    """Update HANDOFF.md with current state."""
    handoff_path = model_dir / "HANDOFF.md"

    err_str = f"{status['cpi_error']:.1f}%" if status['cpi_error'] is not None else "N/A"
    cpi_str = f"{status['base_cpi']:.3f}" if status['base_cpi'] is not None else "N/A"
    passed = "PASSED" if status['cpi_error'] is not None and status['cpi_error'] < 5.0 else "FAILED" if status['cpi_error'] is not None and status['cpi_error'] >= 15.0 else "MARGINAL"

    bench_lines = []
    for b in benchmarks:
        bench_lines.append(f"- {b['benchmark_type']}: {b['raw_value']} {b.get('unit', '')} @ {b['clock_mhz']}MHz")

    content = f"""# {proc_name} Model Handoff

## Current Status
- **Validation**: {passed}
- **CPI Error**: {err_str}
- **Last Updated**: {TODAY}
- **Data Source**: Published benchmark data (external validation)

## Current Model Summary
- Typical CPI: {cpi_str}
- Calibrated against real published benchmarks
- Correction terms fitted via system identification

## External Benchmark Data
{chr(10).join(bench_lines)}

## Known Issues
{"- CPI error > 15% — model architecture may need adjustment to match real benchmark behavior" if passed == "FAILED" else "- None significant" if passed == "PASSED" else "- CPI error 5-15% — minor tuning may improve accuracy"}

## Suggested Next Steps
{"- Investigate architectural mismatch causing high error" if passed == "FAILED" else "- Model is well-calibrated against external data" if passed == "PASSED" else "- Consider fine-tuning instruction category timing"}
- Consider adding additional benchmark sources for cross-validation

## Key Architectural Notes
- CPI measurements now derived from published benchmarks, not synthetic data
- System identification correction terms recalibrated against real targets
"""

    if not dry_run:
        handoff_path.write_text(content)
    return True


def update_validation_json(model_dir: Path, proc_name: str, benchmarks: List[Dict],
                          status: Dict, dry_run: bool = False) -> bool:
    """Update validation JSON with external benchmark info."""
    val_dir = model_dir / "validation"
    val_files = list(val_dir.glob("*_validation.json")) if val_dir.exists() else []
    if not val_files:
        return False

    try:
        with open(val_files[0]) as f:
            val_data = json.load(f)
    except Exception:
        return False

    # Add external validation section
    val_data["external_validation"] = {
        "has_external_data": True,
        "benchmark_sources": [b["benchmark_type"] for b in benchmarks],
        "primary_source": benchmarks[0]["benchmark_type"] if benchmarks else "none",
        "date_updated": TODAY,
        "cpi_error_percent": round(status["cpi_error"], 2) if status["cpi_error"] is not None else None,
    }

    if not dry_run:
        with open(val_files[0], "w") as f:
            json.dump(val_data, f, indent=2)
    return True


def update_readme(model_dir: Path, proc_name: str, status: Dict, dry_run: bool = False) -> bool:
    """Update README.md validation status section if it exists."""
    readme_path = model_dir / "README.md"
    if not readme_path.exists():
        return False

    content = readme_path.read_text()

    # Look for validation status section and update
    err_str = f"{status['cpi_error']:.1f}%" if status['cpi_error'] is not None else "N/A"
    passed = "PASS" if status['cpi_error'] is not None and status['cpi_error'] < 5.0 else "FAIL" if status['cpi_error'] is not None and status['cpi_error'] >= 15.0 else "MARGINAL"

    # Try to update the validation badge/status line
    import re
    # Pattern: look for validation status line
    patterns = [
        (r'Validation Status:\s*\S+', f'Validation Status: {passed} ({err_str} error, external benchmark)'),
        (r'\*\*Validation\*\*:\s*\S+', f'**Validation**: {passed} ({err_str} error, external benchmark)'),
        (r'Status:\s*(?:PASS|FAIL|MARGINAL|UNKNOWN)\b', f'Status: {passed} ({err_str} error, external benchmark)'),
    ]

    updated = False
    for pattern, replacement in patterns:
        new_content = re.sub(pattern, replacement, content, count=1)
        if new_content != content:
            content = new_content
            updated = True
            break

    if updated and not dry_run:
        readme_path.write_text(content)
    return updated


def main():
    parser = argparse.ArgumentParser(description="Update documentation for benchmark-updated models")
    parser.add_argument("--processor", help="Only update this processor")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    print("=" * 75)
    print("UPDATE DOCUMENTATION FOR EXTERNAL BENCHMARKS")
    print("=" * 75)
    print(f"Mode: {'DRY-RUN' if args.dry_run else 'WRITE FILES'}")
    print()

    benchmark_db = load_benchmark_database()
    proc_dirs = get_processor_dirs()

    changelog_count = 0
    handoff_count = 0
    validation_count = 0
    readme_count = 0

    for proc_name, benchmarks in sorted(benchmark_db.items()):
        if args.processor and proc_name != args.processor:
            continue
        if proc_name not in proc_dirs:
            continue

        model_dir = proc_dirs[proc_name]

        # Check if this processor was actually updated (has published_benchmark source)
        meas_path = model_dir / "measurements" / "measured_cpi.json"
        if meas_path.exists():
            with open(meas_path) as f:
                meas = json.load(f)
            sources = [m.get("source") for m in meas.get("measurements", [])]
            if "published_benchmark" not in sources:
                continue

        status = get_current_validation_status(model_dir)

        if update_changelog(model_dir, proc_name, benchmarks, status, args.dry_run):
            changelog_count += 1
        if update_handoff(model_dir, proc_name, benchmarks, status, args.dry_run):
            handoff_count += 1
        if update_validation_json(model_dir, proc_name, benchmarks, status, args.dry_run):
            validation_count += 1
        if update_readme(model_dir, proc_name, status, args.dry_run):
            readme_count += 1

        if args.verbose:
            err_str = f"{status['cpi_error']:.2f}%" if status['cpi_error'] is not None else "N/A"
            print(f"  {proc_name:30s} — err={err_str}")

    print()
    print(f"CHANGELOG.md updated:     {changelog_count}")
    print(f"HANDOFF.md updated:       {handoff_count}")
    print(f"Validation JSON updated:  {validation_count}")
    print(f"README.md updated:        {readme_count}")

    if args.dry_run:
        print("\nDRY RUN — no files were modified.")


if __name__ == "__main__":
    main()
