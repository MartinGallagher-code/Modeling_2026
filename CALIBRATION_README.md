# Item #4: Model Calibration Tools

Tools for calibrating processor models to match expected CPI values from datasheets.

## Overview

After running accuracy tests, most models show significant error (>10%) because they use template timing values. These tools help tune models to match expected performance.

## Tools

### 1. `model_calibrator.py` - Auto-Calibration

Automatically adjusts timing parameters to minimize error.

```bash
# Analyze sensitivity (which parameters matter most)
python model_calibrator.py . --processor i8086 --analyze

# Calibrate a single processor
python model_calibrator.py . --processor i8086 --calibrate

# Calibrate all processors
python model_calibrator.py . --calibrate-all

# Generate calibrated model files
python model_calibrator.py . --processor i8086 --calibrate --generate
```

#### Example Output

```
SENSITIVITY ANALYSIS: i8086
======================================================================

Parameter                           Base Value  Sensitivity   Direction
----------------------------------------------------------------------
branch.base_cycles                       15.00       0.45x    positive
memory_read.base_cycles                   8.00       0.32x    positive
memory_write.base_cycles                  8.00       0.28x    positive

Sensitivity = % change in CPI per % change in parameter
Higher values = more impact on model output
```

### 2. `calibration_report.py` - Status Report

Generates comprehensive calibration status for all processors.

```bash
# View report
python calibration_report.py .

# Export as Markdown
python calibration_report.py . --output calibration_status.md

# Export as JSON
python calibration_report.py . --json > status.json
```

#### Example Output

```
CALIBRATION STATUS REPORT
================================================================================

SUMMARY
----------------------------------------
Total processors:     48
Fully validated (<5%): 2
Close (<10%):         3
Needs calibration:    43
Errors:               0

BY ARCHITECTURE ERA
--------------------------------------------------------------------------------

SEQUENTIAL (1971-1976) - Sequential execution, no prefetch
Expected CPI range: 5.0 - 15.0
Status: 1/8 validated, 2/8 close

  Needs calibration:
    ↓ i8085: 8.15 → 5.50 (+48.2%)
    ↓ m6800: 8.15 → 4.00 (+103.8%)

PREFETCH_QUEUE (1976-1982) - Instruction prefetch queue
Expected CPI range: 3.0 - 7.0
Status: 0/10 validated, 1/10 close

  Needs calibration:
    ↓ i8086: 7.55 → 4.50 (+67.8%)
    ↓ z80: 12.53 → 5.50 (+127.8%)
```

## Calibration Process

### Step 1: Generate Report

```bash
python calibration_report.py . --output status.md
```

Review which processors need work and by how much.

### Step 2: Calibrate Models

```bash
# Option A: Auto-calibrate all
python model_calibrator.py . --calibrate-all --generate

# Option B: Manual calibration per processor
python model_calibrator.py . --processor i8086 --analyze
python model_calibrator.py . --processor i8086 --calibrate --generate
```

### Step 3: Verify Results

```bash
python run_accuracy_tests.py . --verbose
```

### Step 4: Copy Calibrated Files

Auto-calibration creates `*_calibrated.py` files. To use them:

```bash
# Backup original
mv intel/i8086/current/i8086_validated.py intel/i8086/archive/

# Use calibrated version
mv intel/i8086/current/i8086_calibrated.py intel/i8086/current/i8086_validated.py
```

## How Auto-Calibration Works

1. **Load model** and get current predicted CPI
2. **Calculate scale factor**: `expected_cpi / predicted_cpi`
3. **Apply uniform scaling** to all `base_cycles` parameters
4. **Verify improvement** and iterate if needed
5. **Generate calibrated file** with changes documented

### Limitations

- Uses uniform scaling (not per-category tuning)
- May not achieve <5% for complex architectures
- Manual tuning still recommended for best results

## Manual Calibration Guide

For manual calibration, adjust these parameters:

### Sequential Era (i4004, i8080, mos6502, etc.)
- `base_cycles` for each instruction category
- Focus on most frequent categories (ALU, memory)

### Prefetch Queue Era (i8086, z80, etc.)
- `base_cycles` per category
- `bus_cycle_time` - affects memory access
- `prefetch_queue_size` - affects branch penalties

### Pipelined Era (i80286, m68000, etc.)
- `pipeline_stages` - decode, execute, etc.
- `stall_cycles` for various hazards
- Memory access timing

### Cache/RISC Era (i80386+, ARM, SPARC, etc.)
- `cache_hit_cycles` vs `cache_miss_cycles`
- `branch_prediction_accuracy`
- Pipeline depth and bypass paths

## Files

| File | Purpose |
|------|---------|
| `model_calibrator.py` | Auto-calibration and sensitivity analysis |
| `calibration_report.py` | Status report generator |
| `CALIBRATION_README.md` | This documentation |

## Integration with Validation

After calibration, re-run the full validation suite:

```bash
# 1. Run accuracy tests
python run_accuracy_tests.py .

# 2. Check coverage audit
python validation_coverage_audit.py . --verbose

# 3. Generate final report
python calibration_report.py . --output final_status.md
```

Target: Get all processors to <5% error for "Fully Validated" status.
