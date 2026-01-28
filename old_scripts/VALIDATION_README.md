# Validation Coverage Completeness Tools

Comprehensive toolkit for auditing, generating, and running validation tests for the Modeling_2026 processor models.

## Overview

This toolkit ensures all 61 processor models have complete validation coverage across multiple dimensions:

1. **Source Diversity**: Datasheet, emulator, WikiChip, etc.
2. **Timing Tests**: Instruction timing verification
3. **Accuracy Metrics**: IPC/CPI error measurement
4. **Cross-Validation**: Comparison with related processors

## Files

| File | Size | Purpose |
|------|------|---------|
| `validation_coverage_audit.py` | ~35KB | Audit validation coverage completeness |
| `validation_generator.py` | ~25KB | Generate validation JSON templates |
| `validation_runner.py` | ~15KB | Execute validation tests |
| `VALIDATION_README.md` | - | This documentation |

---

## Quick Start

### Step 1: Audit Current Validation Coverage

```bash
# Basic audit
python validation_coverage_audit.py /path/to/Modeling_2026

# Verbose (show all processors)
python validation_coverage_audit.py /path/to/Modeling_2026 --verbose

# JSON output
python validation_coverage_audit.py /path/to/Modeling_2026 --json --output coverage.json
```

### Step 2: Generate Missing Validation Files

```bash
# Generate for all processors
python validation_generator.py /path/to/Modeling_2026 --generate-all

# Generate for specific family
python validation_generator.py /path/to/Modeling_2026 --family intel

# Update sources in existing files
python validation_generator.py /path/to/Modeling_2026 --update-sources
```

### Step 3: Run Validation Tests

```bash
# Run all validations
python validation_runner.py /path/to/Modeling_2026 --run-all --verbose

# Run for specific processor
python validation_runner.py /path/to/Modeling_2026 --processor i8086

# Update JSON with results
python validation_runner.py /path/to/Modeling_2026 --run-all --update-json
```

---

## Validation Levels

The audit system classifies processors into validation levels:

| Level | Name | Criteria |
|-------|------|----------|
| 0 | None | No validation JSON file |
| 1 | Minimal | JSON exists but incomplete |
| 2 | Partial | Has sources but no timing tests |
| 3 | Basic | Has tests but accuracy unknown |
| 4 | Validated | Has accuracy < 10% error |
| 5 | Fully Validated | Has accuracy < 5% with 3+ sources |

---

## Completeness Score (0-100)

The completeness score is calculated from:

| Component | Points | Criteria |
|-----------|--------|----------|
| File presence | 20 | validation.json (10) + validated.py (10) |
| Schema compliance | 10 | All required fields present |
| Source diversity | 25 | Number and types of sources |
| Timing tests | 20 | Number and pass rate of tests |
| Accuracy | 25 | IPC error percentage |

---

## Source Types

The system recognizes these validation source types:

| Type | Weight | Description |
|------|--------|-------------|
| `datasheet` | 3.0 | Original manufacturer datasheet |
| `hardware` | 3.0 | Real hardware measurement |
| `emulator` | 2.5 | Cycle-accurate emulator (MAME, VICE) |
| `mame` | 2.5 | MAME emulator source |
| `vice` | 2.5 | VICE emulator (C64/6502) |
| `programming_manual` | 2.5 | Official programming manual |
| `technical_reference` | 2.5 | Technical reference manual |
| `bitsavers` | 2.0 | Bitsavers documentation |
| `wikichip` | 2.0 | WikiChip specifications |
| `dosbox` | 2.0 | DOSBox emulator (x86) |
| `academic` | 2.0 | Academic paper |
| `wikipedia` | 1.5 | Wikipedia technical article |
| `cpu_world` | 1.5 | CPU-World specifications |

---

## Validation JSON Schema

```json
{
  "processor": "i8086",
  "full_name": "Intel 8086",
  "family": "intel",
  "manufacturer": "Intel",
  "year": 1978,
  "validation_date": "2026-01-27",
  "model_version": "1.0.0",
  "architecture": "prefetch_queue",
  
  "specifications": {
    "clock_mhz": 5.0,
    "transistors": 29000,
    "data_bits": 16,
    "address_bits": 20
  },
  
  "sources": [
    {
      "type": "datasheet",
      "name": "Intel 8086 Datasheet",
      "url": "http://datasheets.chipdb.org/Intel/x86/808x/datashts/8086.pdf",
      "verified": true
    },
    {
      "type": "emulator",
      "name": "DOSBox",
      "url": null,
      "verified": false
    }
  ],
  
  "timing_tests": [
    {
      "name": "NOP_timing",
      "category": "control",
      "description": "NOP instruction timing",
      "expected_cycles": 3,
      "measured_cycles": 3.1,
      "error_percent": 3.3,
      "passed": true,
      "source": "datasheet"
    }
  ],
  
  "accuracy": {
    "ipc_error_percent": 4.2,
    "cpi_error_percent": 3.8,
    "validated_workloads": ["typical", "compute"],
    "notes": "Validated against DOSBox timing"
  },
  
  "instruction_categories": {
    "count": 8,
    "list": ["alu", "memory", "control", "string", "stack", "io", "mul_div", "misc"]
  },
  
  "workload_profiles": {
    "available": ["typical", "compute", "memory", "control"],
    "validated": ["typical", "compute"]
  },
  
  "cross_validation": {
    "processors": ["i8088", "i80186"],
    "notes": "8088 has same timing, 8-bit bus"
  },
  
  "notes": "IBM PC original CPU"
}
```

---

## Processor Specifications Database

The `validation_generator.py` includes a database of known processor specifications with URLs for:

### Intel Family
- 4004, 4040, 8008, 8080, 8085, 8086, 8088, 80186, 80286, 80386

### Motorola Family
- 6800, 6809, 68000, 68020

### MOS/WDC Family
- 6502, 6510, 65C02, 65816

### Zilog Family
- Z80, Z8000

### Other
- ARM1, SPARC, MIPS R2000, Am2901, Am29000, F8, RCA 1802, SC/MP, Signetics 2650, TMS9900, NS32016, T414

View the database:
```bash
python validation_generator.py --list-specs
```

---

## Accuracy Thresholds

| Level | Threshold | Classification |
|-------|-----------|----------------|
| Excellent | < 2% | Research-grade accuracy |
| Good | < 5% | Validated model |
| Acceptable | < 10% | Usable model |
| Poor | < 20% | Needs improvement |
| Failing | ≥ 20% | Requires revalidation |

---

## Standard Timing Tests

### All Architectures
- `NOP_timing`: NOP instruction
- `register_move`: Register to register
- `memory_load`: Load from memory
- `memory_store`: Store to memory
- `add_register`: ALU operation
- `branch_taken`: Branch when taken
- `branch_not_taken`: Branch when not taken

### Prefetch Queue Architecture
- `queue_hit`: Instruction in prefetch queue
- `queue_miss`: Instruction not in queue

### Pipelined Architecture
- `pipeline_stall`: Pipeline stall on hazard

### Cache/RISC Architecture
- `cache_hit`: L1 cache hit (typically 1 cycle)
- `cache_miss`: L1 cache miss

---

## Example Workflow

```bash
# 1. Initial audit
python validation_coverage_audit.py . --verbose > initial_audit.txt

# 2. Generate missing validation files
python validation_generator.py . --generate-all --dry-run
python validation_generator.py . --generate-all

# 3. Add known source URLs
python validation_generator.py . --update-sources

# 4. Run validation tests
python validation_runner.py . --run-all --verbose

# 5. Update validation JSON with results
python validation_runner.py . --run-all --update-json

# 6. Final audit
python validation_coverage_audit.py . --json --output final_coverage.json

# 7. Check specific processor
python validation_coverage_audit.py . --verbose | grep -A5 "i8086"
```

---

## Report Interpretation

### Executive Summary
```
EXECUTIVE SUMMARY
----------------------------------------
Total Processors: 61
Fully Validated (<5% error, 3+ sources): 12 (19.7%)
Validated (<10% error): 35 (57.4%)
Average Completeness Score: 68.5/100
```

### Level Distribution
```
VALIDATION LEVEL DISTRIBUTION
----------------------------------------
  No Validation                      5 █████
  Minimal (JSON only)                8 ████████
  Partial (sources, no tests)       10 ██████████
  Basic (tests, accuracy unknown)   18 ██████████████████
  Validated (<10% error)            15 ███████████████
  Fully Validated (<5% error)        5 █████
```

### Recommendations
```
TOP RECOMMENDATIONS
----------------------------------------
  [25 processors] Add datasheet sources
  [18 processors] Add emulator validation
  [15 processors] Add more timing tests
  [12 processors] Improve model accuracy
```

---

## Integration with CI/CD

Add to your CI pipeline:

```yaml
# .github/workflows/validation.yml
name: Validation Coverage

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Run Validation Audit
        run: |
          python validation_coverage_audit.py . --json --output coverage.json
          
      - name: Check Coverage Threshold
        run: |
          # Fail if less than 50% validated
          python -c "
          import json
          with open('coverage.json') as f:
              data = json.load(f)
          rate = data['summary']['validation_rate_percent']
          if rate < 50:
              print(f'Validation rate {rate}% is below 50% threshold')
              exit(1)
          print(f'Validation rate: {rate}%')
          "
```

---

## Troubleshooting

### "No validation JSON file found"
Run the generator:
```bash
python validation_generator.py . --generate-all
```

### "Failed to load model"
Check the model file for syntax errors:
```bash
python -m py_compile intel/i8086/current/i8086_validated.py
```

### "No timing tests defined"
Edit the validation JSON to add timing tests with expected values from the datasheet.

### "Accuracy unknown"
Run the validation runner with `--update-json`:
```bash
python validation_runner.py . --processor i8086 --update-json
```

---

## Requirements

- Python 3.8+
- No external dependencies (uses only standard library)

---

## Author

Grey-Box Performance Modeling Research Project  
January 2026
