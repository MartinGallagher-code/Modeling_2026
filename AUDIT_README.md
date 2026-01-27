# Cross-Family Consistency Audit Tools

Tools for auditing and fixing consistency issues across all 61 processor models in the Modeling_2026 repository.

## Overview

These scripts help maintain consistency across the 5 processor families (Intel, Motorola, MOS/WDC, Zilog, Other) by:

1. **Auditing** - Identifying structural, naming, interface, and documentation inconsistencies
2. **Fixing** - Automatically generating missing files and fixing common issues

## Files

| File | Purpose |
|------|---------|
| `cross_family_audit.py` | Main audit script - scans repository and reports issues |
| `apply_consistency_fixes.py` | Fix application script - applies recommended fixes |
| `run_audit.sh` | Convenience wrapper script |

## Quick Start

### 1. Run Audit Only

```bash
# Basic audit
python cross_family_audit.py /path/to/Modeling_2026

# Verbose audit (shows per-processor details)
python cross_family_audit.py /path/to/Modeling_2026 --verbose

# Save report to file
python cross_family_audit.py /path/to/Modeling_2026 --output audit_report.txt
```

### 2. Apply All Fixes (Dry Run First!)

```bash
# See what would change without making changes
python apply_consistency_fixes.py /path/to/Modeling_2026 --fix-all --dry-run

# Apply all fixes with backups
python apply_consistency_fixes.py /path/to/Modeling_2026 --fix-all

# Apply without backups (use with caution)
python apply_consistency_fixes.py /path/to/Modeling_2026 --fix-all --no-backup
```

### 3. Apply Specific Fixes

```bash
# Create missing directories only
python apply_consistency_fixes.py /path/to/Modeling_2026 --fix-structure

# Generate missing READMEs
python apply_consistency_fixes.py /path/to/Modeling_2026 --fix-readme

# Generate missing validation JSONs
python apply_consistency_fixes.py /path/to/Modeling_2026 --fix-json

# Create/update base model class
python apply_consistency_fixes.py /path/to/Modeling_2026 --fix-base

# Add method stubs to incomplete models
python apply_consistency_fixes.py /path/to/Modeling_2026 --fix-stubs

# Create __init__.py files
python apply_consistency_fixes.py /path/to/Modeling_2026 --fix-init

# Update index.json
python apply_consistency_fixes.py /path/to/Modeling_2026 --fix-index
```

## What Gets Audited

### Directory Structure
Each processor should have:
```
[processor]/
├── README.md
├── current/
│   └── [processor]_validated.py
├── archive/
├── validation/
│   └── [processor]_validation.json
└── docs/
```

### Python Model Interface
All `*_validated.py` files should implement:
- `analyze(workload: str) -> AnalysisResult`
- `validate() -> Dict`
- `get_instruction_categories() -> Dict`
- `get_workload_profiles() -> Dict`

### Validation JSON Schema
Required keys:
- `processor`
- `validation_date`
- `sources`
- `timing_tests`
- `accuracy`

### Model Design Guidelines
- Maximum 15 instruction categories (based on research finding)
- Standard workload profiles: `typical`, `compute`, `memory`, `control`
- Consistent class naming within families

## Issue Severity Levels

| Level | Meaning |
|-------|---------|
| ❌ Error | Must fix - breaks consistency or functionality |
| ⚠️ Warning | Should fix - reduces quality or maintainability |
| ℹ️ Info | Consider fixing - minor improvement opportunity |

## Generated Files

### base_model.py
Located in `common/base_model.py`, provides:
- `BaseProcessorModel` - Abstract base class for all models
- `InstructionCategory` - Dataclass for instruction categories
- `WorkloadProfile` - Dataclass for workload definitions
- `AnalysisResult` - Dataclass for analysis results

### README Templates
Auto-generated READMEs include:
- Model overview
- File structure
- Usage example
- Validation checklist

### Validation JSON Templates
Auto-generated validation files include:
- Processor identification
- Source placeholders
- Test structure
- Accuracy fields

## Example Workflow

```bash
# 1. Clone/download your repository
cd /path/to/Modeling_2026

# 2. Copy audit scripts to repository
cp cross_family_audit.py apply_consistency_fixes.py ./

# 3. Run initial audit
python cross_family_audit.py . --verbose > initial_audit.txt

# 4. Review issues
cat initial_audit.txt

# 5. Dry run fixes
python apply_consistency_fixes.py . --fix-all --dry-run

# 6. Apply fixes
python apply_consistency_fixes.py . --fix-all

# 7. Run audit again to verify
python cross_family_audit.py . --verbose

# 8. Commit changes
git add -A
git commit -m "Apply consistency fixes from cross-family audit"
```

## Customization

### Adding Custom Checks
Edit `cross_family_audit.py` and add to the `audit_*` functions.

### Modifying Templates
Edit the `generate_*_template()` functions in `cross_family_audit.py`.

### Changing Standards
Modify the configuration constants at the top of `cross_family_audit.py`:
- `EXPECTED_FAMILIES`
- `EXPECTED_SUBDIRS`
- `REQUIRED_METHODS`
- `STANDARD_WORKLOADS`
- `MAX_RECOMMENDED_CATEGORIES`

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success (no errors found) |
| 1 | Errors found (or fix errors) |

## Requirements

- Python 3.8+
- No external dependencies (uses only standard library)

## Author

Grey-Box Performance Modeling Research Project
January 2026
