# Modeling_2026 Audit & Fix Tools

Comprehensive tools for auditing and improving the processor models in the Modeling_2026 repository.

## Overview

This toolkit provides two complementary systems:

### 1. Cross-Family Consistency Audit
Identifies structural, naming, interface, and documentation inconsistencies across all 5 processor families.

### 2. Era-Specific Architecture Audit
Verifies each processor uses the correct queueing model architecture for its era:
- **Sequential (1971-1976)**: Simple serial M/M/1 chain
- **Prefetch Queue (1976-1982)**: Parallel BIU/EU queues
- **Pipelined (1979-1985)**: Multi-stage pipeline network
- **Cache/RISC (1983-1988)**: Cache hierarchy + deep pipeline

## Files

| File | Size | Purpose |
|------|------|---------|
| `cross_family_audit.py` | ~20KB | Cross-family consistency audit |
| `apply_consistency_fixes.py` | ~12KB | Apply consistency fixes |
| `era_architectures.py` | ~54KB | Era definitions and queueing models |
| `era_architecture_audit.py` | ~21KB | Era-specific architecture audit |
| `apply_era_fixes.py` | ~26KB | Generate era-appropriate templates |
| `AUDIT_README.md` | - | This documentation |

---

## Quick Start

### Step 1: Copy files to your repository
```bash
cd /path/to/Modeling_2026
cp cross_family_audit.py apply_consistency_fixes.py .
cp era_architectures.py era_architecture_audit.py apply_era_fixes.py .
```

### Step 2: Run cross-family audit
```bash
python cross_family_audit.py . --verbose
```

### Step 3: Apply consistency fixes
```bash
# Preview changes first
python apply_consistency_fixes.py . --fix-all --dry-run

# Apply changes
python apply_consistency_fixes.py . --fix-all
```

### Step 4: Run era-specific audit
```bash
python era_architecture_audit.py . --verbose
```

### Step 5: Generate era-appropriate templates
```bash
# Preview first
python apply_era_fixes.py . --fix-mismatched --dry-run

# Apply
python apply_era_fixes.py . --fix-mismatched
```

---

## Part 1: Cross-Family Consistency Audit

### What Gets Checked

**Directory Structure:**
```
processor/
├── README.md          (recommended)
├── current/           (required)
│   └── *_validated.py
├── validation/        (required)
│   └── *_validation.json
├── docs/              (recommended)
└── archive/           (recommended)
```

**Python Model Interface:**
- Required methods: `analyze()`, `validate()`, `get_instruction_categories()`, `get_workload_profiles()`
- Required attributes: `name`, `manufacturer`, `year`, `clock_mhz`, `transistor_count`
- Category count: warns if >15 (per research finding)
- Standard workloads: `typical`, `compute`, `memory`, `control`

**Validation JSON Schema:**
- Required keys: `processor`, `validation_date`, `sources`, `timing_tests`, `accuracy`
- Warns if IPC error >5%

### Command Options

```bash
# Basic audit
python cross_family_audit.py /path/to/repo

# Verbose (per-processor details)
python cross_family_audit.py /path/to/repo --verbose

# Save to file
python cross_family_audit.py /path/to/repo --output audit_report.txt

# JSON output
python cross_family_audit.py /path/to/repo --json
```

### Fix Options

```bash
# Apply all fixes
python apply_consistency_fixes.py . --fix-all

# Selective fixes
python apply_consistency_fixes.py . --fix-structure   # Create directories
python apply_consistency_fixes.py . --fix-readme      # Generate READMEs
python apply_consistency_fixes.py . --fix-json        # Generate validation JSON
python apply_consistency_fixes.py . --fix-base        # Create base_model.py
python apply_consistency_fixes.py . --fix-init        # Create __init__.py files
python apply_consistency_fixes.py . --fix-index       # Create index.json

# Always dry-run first!
python apply_consistency_fixes.py . --fix-all --dry-run
```

---

## Part 2: Era-Specific Architecture Audit

### Era Definitions

| Era | Years | Queueing Model | Example Processors |
|-----|-------|----------------|-------------------|
| **Sequential** | 1971-1976 | Serial M/M/1 chain | 4004, 8008, 8080, 6502, 6800 |
| **Prefetch Queue** | 1976-1982 | Parallel BIU/EU | 8086, 8088, Z80, 6809 |
| **Pipelined** | 1979-1985 | Pipeline network | 68000, 80286, Z80000 |
| **Cache/RISC** | 1983-1988 | Cache + pipeline | ARM1, SPARC, MIPS, 80386 |

### Architecture Diagrams

**Sequential (1971-1976):**
```
FETCH → DECODE → EXECUTE → MEMORY (serial)
CPI = sum of stage times
```

**Prefetch Queue (1976-1982):**
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

**Pipelined (1979-1985):**
```
IF → ID → OF → EX → WB (parallel stages)
Ideal CPI = 1.0
Actual CPI = 1.0 + hazards + stalls
```

**Cache/RISC (1983-1988):**
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

### Command Options

```bash
# Show era summary
python era_architectures.py

# Run audit
python era_architecture_audit.py /path/to/repo --verbose

# JSON output
python era_architecture_audit.py /path/to/repo --json --output era_audit.json
```

### Template Generation

```bash
# Fix only processors with mismatched architectures
python apply_era_fixes.py . --fix-mismatched

# Generate templates for ALL processors
python apply_era_fixes.py . --generate-all

# Fix specific processor
python apply_era_fixes.py . --processor i8086

# Always dry-run first!
python apply_era_fixes.py . --fix-mismatched --dry-run
```

---

## Complete Workflow

```bash
# 1. Setup
cd /path/to/Modeling_2026
# Copy all 5 Python files here

# 2. Reorganize into family structure (if needed)
mkdir -p intel motorola mos_wdc zilog other common
mv 8086 intel/i8086  # etc.

# 3. Run cross-family audit
python cross_family_audit.py . --verbose > consistency_audit.txt

# 4. Apply consistency fixes
python apply_consistency_fixes.py . --fix-all --dry-run
python apply_consistency_fixes.py . --fix-all

# 5. Run era-specific audit
python era_architecture_audit.py . --verbose > era_audit.txt

# 6. Generate era-appropriate templates
python apply_era_fixes.py . --fix-mismatched --dry-run
python apply_era_fixes.py . --fix-mismatched

# 7. Verify
python cross_family_audit.py .
python era_architecture_audit.py .

# 8. Commit
git add -A
git commit -m "Apply audit fixes and era-specific architecture patterns"
git push
```

---

## Processor Era Mapping

### Sequential Era (27 processors)
- **Intel:** 4004, 4040, 8008, 8048, 8051, 8080, 8085, 8748, 8751
- **Motorola:** 6800, 6801, 6802, 6805
- **MOS/WDC:** 6502, 6510, 65C02
- **Zilog:** Z8
- **Other:** Am2901, Am2903, F8, 1802, 1805, SC/MP, 2650, 9900, 9995, NC4016

### Prefetch Queue Era (13 processors)
- **Intel:** 8086, 8088, 80186, 80188, 80287
- **Motorola:** 6809, 68HC11
- **MOS/WDC:** 65816
- **Zilog:** Z80, Z80A, Z80B, Z180, Z8000

### Pipelined Era (17 processors)
- **Intel:** 80286, iAPX 432
- **Motorola:** 68000, 68008, 68010, 68020, 68881, 68882
- **Zilog:** Z80000
- **Other:** NS32016, NS32032, TMS320C10, WE32000, RTX2000

### Cache/RISC Era (35 processors)
- **Intel:** 80386, 80387, 80486, i860, Pentium
- **Motorola:** 68030, 68040, 68060
- **Other:** ARM1, ARM2, ARM3, ARM6, MIPS R2000, SPARC, Am29000, Alpha 21064, HP PA-RISC, PowerPC 601, T414, T800

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success (no errors) |
| 1 | Errors found |

---

## Requirements

- Python 3.8+
- No external dependencies (uses only standard library)

---

## Author

Grey-Box Performance Modeling Research Project  
January 2026
