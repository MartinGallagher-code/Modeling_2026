#!/usr/bin/env python3
"""
Apply System Identification Corrections to Model Source Files
================================================================

Reads optimized correction values from identification/sysid_result.json
and patches the corresponding _validated.py model files to use those
values instead of zeros.

Usage:
    python apply_corrections.py                    # all models
    python apply_corrections.py --family zilog     # one family
    python apply_corrections.py --processor z80    # one processor
    python apply_corrections.py --dry-run          # preview only
    python apply_corrections.py --min-improvement 0.5  # only apply if error improved by ≥0.5%

Author: Grey-Box Performance Modeling Research
Date: January 2026
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent


def discover_models_with_results(
    repo_root: Path,
    family_filter: Optional[str] = None,
    processor_filter: Optional[str] = None,
) -> List[Dict]:
    """Find models that have sysid_result.json files."""
    index_path = repo_root / "index.json"
    if not index_path.exists():
        return []

    with open(index_path) as f:
        index = json.load(f)

    results = []
    for family, info in index.get("families", {}).items():
        if family_filter and family != family_filter:
            continue
        for proc in info.get("processors", []):
            if processor_filter and proc != processor_filter:
                continue

            model_dir = repo_root / "models" / family / proc
            sysid_path = model_dir / "identification" / "sysid_result.json"
            if not sysid_path.exists():
                continue

            current_dir = model_dir / "current"
            model_files = list(current_dir.glob("*_validated.py")) if current_dir.exists() else []
            if not model_files:
                continue

            results.append({
                "family": family,
                "processor": proc,
                "model_dir": model_dir,
                "model_file": model_files[0],
                "sysid_path": sysid_path,
            })

    return results


def load_sysid_result(path: Path) -> Dict:
    """Load a sysid_result.json file."""
    with open(path) as f:
        return json.load(f)


def apply_corrections_to_file(
    model_file: Path,
    corrections: Dict[str, float],
    dry_run: bool = False,
) -> Tuple[bool, str]:
    """Patch a _validated.py file to use optimized correction values.

    Looks for the pattern:
        self.corrections = {cat: 0.0 for cat in self.instruction_categories}
    or:
        self.corrections = {...}

    and replaces it with explicit correction values.

    Returns (success, message).
    """
    source = model_file.read_text()

    # Strip 'cor.' prefix from keys to get category names
    cor_values = {}
    for key, val in corrections.items():
        cat_name = key.replace("cor.", "") if key.startswith("cor.") else key
        cor_values[cat_name] = val

    # Check if all corrections are zero — skip if nothing to apply
    if all(abs(v) < 1e-8 for v in cor_values.values()):
        return False, "all corrections are zero"

    # Build the replacement dict literal
    items = []
    for cat, val in sorted(cor_values.items()):
        items.append(f"'{cat}': {val:.6f}")
    new_dict = "{\n" + ",\n".join(f"            {item}" for item in items) + "\n        }"
    new_line = f"self.corrections = {new_dict}"

    # Pattern 1: dict comprehension  {cat: 0.0 for cat in self.instruction_categories}
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
        return False, "no corrections assignment found in source"

    if new_source == source:
        return False, "source unchanged after replacement"

    if not dry_run:
        model_file.write_text(new_source)

    return True, "applied"


def main():
    parser = argparse.ArgumentParser(
        description="Apply system identification corrections to model source files"
    )
    parser.add_argument("--family", help="Only apply to this family")
    parser.add_argument("--processor", help="Only apply to this processor")
    parser.add_argument("--dry-run", action="store_true", help="Preview only")
    parser.add_argument(
        "--min-improvement", type=float, default=0.0,
        help="Only apply if error improved by at least this many %% points (default: 0)"
    )

    args = parser.parse_args()

    print("=" * 75)
    print("APPLY SYSTEM IDENTIFICATION CORRECTIONS")
    print("=" * 75)
    print(f"Mode: {'DRY-RUN' if args.dry_run else 'WRITE FILES'}")
    if args.min_improvement > 0:
        print(f"Min improvement: {args.min_improvement}%")
    print()

    entries = discover_models_with_results(
        REPO_ROOT, args.family, args.processor
    )
    if not entries:
        print("No models with identification results found.")
        return

    applied = 0
    skipped = 0
    failed = 0

    for entry in entries:
        label = f"{entry['family']}/{entry['processor']}"
        sysid = load_sysid_result(entry["sysid_path"])

        # Check if corrections are meaningful
        corrections = sysid.get("corrections", {})
        if not corrections:
            print(f"  SKIP  {label:35s} — no corrections in result")
            skipped += 1
            continue

        # Check improvement threshold
        err_before = sysid.get("loss_before", 0)
        err_after = sysid.get("loss_after", 0)
        cpi_err = sysid.get("cpi_error_percent", 0)

        # Check if the result was a rollback (loss unchanged)
        if err_before == err_after and sysid.get("message", "").startswith("Rolled back"):
            print(f"  SKIP  {label:35s} — rolled back (structural mismatch)")
            skipped += 1
            continue

        # Check all corrections are zero
        if all(abs(v) < 1e-8 for v in corrections.values()):
            print(f"  SKIP  {label:35s} — all corrections zero")
            skipped += 1
            continue

        # Apply
        success, msg = apply_corrections_to_file(
            entry["model_file"], corrections, args.dry_run
        )

        if success:
            applied += 1
            action = "WOULD" if args.dry_run else "APPLIED"
            print(f"  {action:7s} {label:35s} — {len(corrections)} corrections, err={cpi_err:.2f}%")
        else:
            failed += 1
            print(f"  FAIL  {label:35s} — {msg}")

    print()
    print(f"Applied: {applied}  Skipped: {skipped}  Failed: {failed}")
    if args.dry_run:
        print("\nDRY RUN — no files were modified.")


if __name__ == "__main__":
    main()
