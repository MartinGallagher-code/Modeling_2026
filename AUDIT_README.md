# Modeling_2026 Audit & Fix Tools

Comprehensive tools for auditing and improving the 61 processor models in the Modeling_2026 repository.

## Overview

This toolkit provides two complementary systems:

### 1. Cross-Family Consistency Audit
Identifies structural, naming, interface, and documentation inconsistencies across all 5 processor families.

### 2. Era-Specific Architecture Audit
Verifies each processor uses the correct queueing model architecture for its era:
- **Sequential (1971-1976)**: Simple serial M/M/1 chain (27 processors)
- **Prefetch Queue (1976-1982)**: Parallel BIU/EU queues (13 processors)
- **Pipelined (1979-1985)**: Multi-stage pipeline network (14 processors)
- **Cache/RISC (1983-1988)**: Cache hierarchy + deep pipeline (8 processors)

## Files

| File | Size | Purpose |
|------|------|---------|
| `cross_family_audit.py` | 47KB | Cross-family consistency audit |
| `apply_consistency_fixes.py` | 19KB | Apply consistency fixes |
| `era_architectures.py` | 54KB | Era definitions and queueing models |
| `era_architecture_audit.py` | 21KB | Era-specific architecture audit |
| `apply_era_fixes.py` | 26KB | Generate era-appropriate templates |
| `run_audit.sh` | 1.3KB | Convenience wrapper |
| `AUDIT_README.md` | - | This documentation |

---

## Part 1: Cross-Family Consistency Audit

### Quick Start

```bash
# Run audit
python cross_family_audit.py /path/to/Modeling_2026 --verbose

# Preview fixes (dry run)
python apply_consistency_fixes.py /path/to/Modeling_2026 --fix-all --dry-run

# Apply fixes
python apply_consistency_fixes.py /path/to/Modeling_2026 --fix-all
```

### What Gets Checked

- Directory structure (`current/`, `validation/`, `docs/`, `archive/`)
- File naming (`*_validated.py`, `*_validation.json`)
- Python interface (required methods: `analyze`, `validate`, etc.)
- Validation JSON schema
- README documentation

---

## Part 2: Era-Specific Architecture Audit

### Era Definitions

| Era | Years | Queueing Model | Example Processors |
|-----|-------|----------------|-------------------|
| Sequential | 1971-1976 | Serial M/M/1 chain | 4004, 8008, 8080, 6502, 6800 |
| Prefetch Queue | 1976-1982 | Parallel BIU/EU | 8086, 8088, Z80, 6809 |
| Pipelined | 1979-1985 | Pipeline network | 68000, 80286, Z80000 |
| Cache/RISC | 1983-1988 | Cache + pipeline | ARM1, SPARC, MIPS, 80386 |

### Quick Start

```bash
# Show era summary
python era_architectures.py

# Run era audit
python era_architecture_audit.py /path/to/Modeling_2026 --verbose

# Preview template generation (dry run)
python apply_era_fixes.py /path/to/Modeling_2026 --fix-mismatched --dry-run

# Generate templates for mismatched processors
python apply_era_fixes.py /path/to/Modeling_2026 --fix-mismatched

# Generate templates for ALL processors
python apply_era_fixes.py /path/to/Modeling_2026 --generate-all
```

### Architecture Templates

Each era has a specific queueing model template:

**Sequential Architecture:**
```
FETCH → DECODE → EXECUTE → MEMORY (serial)
CPI = sum of stage times
```

**Prefetch Queue Architecture:**
```
┌─────────┐     ┌──────────────┐
│   BIU   │────►│ Prefetch Q   │
└─────────┘     └──────┬───────┘
                       ▼
               ┌──────────────┐
               │     EU       │
               └──────────────┘

CPI = max(BIU, EU) + contention
```

**Pipelined Architecture:**
```
IF → ID → OF → EX → WB (parallel stages)
Ideal CPI = 1.0
Actual CPI = 1.0 + hazards + stalls
```

**Cache/RISC Architecture:**
```
┌─────────┐
│ I-Cache │
└────┬────┘
     ▼
IF → ID → EX → MEM → WB
              ↓
         ┌────────┐
         │D-Cache │
         └────────┘

RISC goal CPI ≈ 1.0
```

---

## Complete Workflow

```bash
# 1. Copy all audit scripts to your repository
cd /path/to/Modeling_2026
cp cross_family_audit.py apply_consistency_fixes.py \
   era_architectures.py era_architecture_audit.py apply_era_fixes.py ./

# 2. Run cross-family consistency audit
python cross_family_audit.py . --verbose > consistency_audit.txt
cat consistency_audit.txt

# 3. Apply consistency fixes (dry run first!)
python apply_consistency_fixes.py . --fix-all --dry-run
python apply_consistency_fixes.py . --fix-all

# 4. Run era-specific architecture audit
python era_architecture_audit.py . --verbose > era_audit.txt
cat era_audit.txt

# 5. Generate era-appropriate templates for mismatched processors
python apply_era_fixes.py . --fix-mismatched --dry-run
python apply_era_fixes.py . --fix-mismatched

# 6. Verify all audits pass
python cross_family_audit.py . 
python era_architecture_audit.py .

# 7. Commit changes
git add -A
git commit -m "Apply consistency and era-specific architecture fixes"
```

---

## Processor Era Mapping

All 61 processors are mapped to their correct architectural era:

### Sequential Era (27 processors)
Intel: 4004, 4040, 8008, 8048, 8051, 8080, 8085, 8748, 8751  
Motorola: 6800, 6801, 6802, 6805  
MOS/WDC: 6502, 6510, 65C02  
Zilog: Z8  
Other: Am2901, Am2903, F8, 1802, 1805, SC/MP, 2650, 9900, 9995, NC4016

### Prefetch Queue Era (13 processors)
Intel: 8086, 8088, 80186, 80188, 80287  
Motorola: 6809, 68HC11  
MOS/WDC: 65816  
Zilog: Z80, Z80A, Z80B, Z180, Z8000

### Pipelined Era (14 processors)
Intel: 80286, iAPX 432  
Motorola: 68000, 68008, 68010, 68020, 68881, 68882  
Zilog: Z80000  
Other: NS32016, NS32032, TMS320C10, WE32000, RTX2000

### Cache/RISC Era (8 processors)
Intel: 80386, 80387  
Other: ARM1, MIPS R2000, SPARC, Am29000, T414, T800

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
