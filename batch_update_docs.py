#!/usr/bin/env python3
"""
Batch Update Documentation for System Identification
======================================================

Appends a CHANGELOG entry and rewrites HANDOFF.md for all models
that have system identification results.

Skips models that already have a 2026-01-29 sysid entry in CHANGELOG.

Usage:
    python batch_update_docs.py                # all models
    python batch_update_docs.py --dry-run      # preview only
"""

import argparse
import json
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
TODAY = date.today().isoformat()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    updated = 0
    skipped = 0
    created = 0

    for sysid_path in sorted(REPO_ROOT.glob("models/**/identification/sysid_result.json")):
        model_dir = sysid_path.parent.parent
        family = model_dir.parent.name
        proc = model_dir.name

        with open(sysid_path) as f:
            sysid = json.load(f)

        corrections = sysid.get("corrections", {})
        converged = sysid.get("converged", False)
        cpi_err = sysid.get("cpi_error_percent", 0)
        loss_before = sysid.get("loss_before", 0)
        loss_after = sysid.get("loss_after", 0)
        n_free = len(sysid.get("free_parameters", []))
        iterations = sysid.get("iterations", 0)
        message = sysid.get("message", "")

        # Check if this is a rollback (no improvement)
        is_rollback = "Rolled back" in message

        # --- CHANGELOG ---
        changelog_path = model_dir / "CHANGELOG.md"
        if changelog_path.exists():
            existing = changelog_path.read_text()
            # Skip if already documented
            if "System identification" in existing and "2026-01-29" in existing:
                skipped += 1
                continue
        else:
            existing = f"# {proc.upper()} Model Changelog\n\nThis file contains the complete history of all work on this model.\n**Append-only: Never delete previous entries.**\n\n---\n"
            created += 1

        # Build changelog entry
        n_nonzero = sum(1 for v in corrections.values() if abs(v) > 1e-6)
        status = "PASSED" if cpi_err < 5 else "MARGINAL" if cpi_err < 15 else "FAILED"

        if is_rollback:
            entry_lines = [
                f"\n## {TODAY} - System identification (rolled back)",
                "",
                "**Session goal:** Fit correction terms via scipy.optimize.least_squares",
                "",
                "**Result:** Optimization was rolled back because it worsened typical-workload error.",
                f"- {n_free} free correction parameters",
                f"- Structural mismatch between workload profiles and measurements",
                f"- Model left unchanged",
                "",
                f"**Final state:**",
                f"- CPI error: {cpi_err:.2f}%",
                f"- Validation: {status}",
                "",
                "---",
            ]
        else:
            cor_summary = ", ".join(
                f"{k.replace('cor.', '')}: {v:+.2f}"
                for k, v in sorted(corrections.items())
                if abs(v) > 0.01
            )
            if not cor_summary:
                cor_summary = "all near zero (model already matched measurements)"

            entry_lines = [
                f"\n## {TODAY} - System identification: correction terms applied",
                "",
                "**Session goal:** Fit correction terms via scipy.optimize.least_squares",
                "",
                f"**Changes made:**",
                f"- Ran system identification with {n_free} free correction parameters",
                f"- Optimizer {'converged' if converged else 'did not converge'} in {iterations} evaluations",
                f"- Corrections: {cor_summary}",
                "",
                f"**Final state:**",
                f"- CPI error: {cpi_err:.2f}%",
                f"- Validation: {status}",
                "",
                "---",
            ]

        entry = "\n".join(entry_lines)

        if not args.dry_run:
            # Append to changelog
            with open(changelog_path, "a") as f:
                f.write(entry + "\n")

        # --- HANDOFF ---
        handoff_path = model_dir / "HANDOFF.md"
        if handoff_path.exists():
            old_handoff = handoff_path.read_text()
        else:
            old_handoff = ""

        # Only rewrite HANDOFF if it doesn't already mention system identification
        if "System identification" not in old_handoff and "sysid" not in old_handoff.lower():
            # Add a section about sysid status to existing HANDOFF
            sysid_section = (
                f"\n## System Identification ({TODAY})\n"
                f"- **Status**: {'Converged' if converged else 'Rolled back' if is_rollback else 'Did not converge'}\n"
                f"- **CPI Error**: {cpi_err:.2f}%\n"
                f"- **Free Parameters**: {n_free}\n"
                f"- **Corrections**: See `identification/sysid_result.json`\n"
            )
            if not args.dry_run:
                with open(handoff_path, "a") as f:
                    f.write(sysid_section)

        updated += 1
        action = "WOULD" if args.dry_run else "UPDATED"
        print(f"  {action:7s} {family}/{proc:30s}  err={cpi_err:.2f}%  conv={'Y' if converged else 'N'}")

    print()
    print(f"Updated: {updated}  Skipped (already documented): {skipped}  Created new: {created}")
    if args.dry_run:
        print("DRY RUN — no files modified.")


if __name__ == "__main__":
    main()
