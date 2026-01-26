# Model Validation Framework

## Overview

A systematic framework for validating processor model predictions against real-world data from emulators, benchmarks, datasheets, and hardware measurements.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         VALIDATION FRAMEWORK                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐        │
│  │  Data Sources   │    │ Validation Cases│    │  Model Interface │        │
│  │                 │    │                 │    │                 │        │
│  │ • Emulators     │───▶│ • Processor     │◀───│ • analyze()     │        │
│  │ • Benchmarks    │    │ • Workload      │    │ • compare()     │        │
│  │ • Datasheets    │    │ • Measured vals │    │ • predict()     │        │
│  │ • Hardware      │    │ • Threshold     │    │                 │        │
│  └─────────────────┘    └────────┬────────┘    └─────────────────┘        │
│                                  │                                         │
│                                  ▼                                         │
│                    ┌─────────────────────────┐                            │
│                    │   Validation Engine     │                            │
│                    │                         │                            │
│                    │ • Run test cases        │                            │
│                    │ • Compare pred vs meas  │                            │
│                    │ • Calculate errors      │                            │
│                    │ • Generate reports      │                            │
│                    └────────────┬────────────┘                            │
│                                 │                                          │
│                                 ▼                                          │
│                    ┌─────────────────────────┐                            │
│                    │   Validation Report     │                            │
│                    │                         │                            │
│                    │ • Pass/Fail counts      │                            │
│                    │ • Error statistics      │                            │
│                    │ • By-processor breakdown│                            │
│                    │ • Detailed results      │                            │
│                    └─────────────────────────┘                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Key Components

### 1. Data Sources (`ValidationSource`)

Represents where validation data comes from:

| Source Type | Examples | Reliability |
|-------------|----------|-------------|
| **Emulator** | MAME, VICE, DOSBox, Hatari | High (0.85-0.95) |
| **Benchmark** | Dhrystone, Whetstone, BYTE Sieve | Medium (0.80) |
| **Datasheet** | Intel, Motorola, Zilog docs | High (0.95) |
| **Hardware** | Direct measurement | Varies |
| **Publication** | BYTE Magazine, academic papers | Medium (0.80) |

```python
source = ValidationSource(
    name="MAME",
    source_type=DataSource.EMULATOR,
    description="Cycle-accurate multi-system emulator",
    url="https://www.mamedev.org/",
    reliability_score=0.95
)
```

### 2. Measured Results (`MeasuredResult`)

A single measured value from a source:

```python
result = MeasuredResult(
    metric=MetricType.CPI,
    value=12.5,
    unit="cycles/instruction",
    uncertainty=0.5,  # ± 0.5
    source=mame_source,
    conditions={"workload": "mixed_dos"}
)
```

### 3. Validation Cases (`ValidationCase`)

A complete test case with processor, conditions, and expected results:

```python
case = ValidationCase(
    id="8086_mame_cycles",
    processor="Intel 8086",
    description="Cycle counts verified against MAME",
    workload_name="typical",
    clock_mhz=5.0,
    measured_results=[
        MeasuredResult(metric=MetricType.CPI, value=12.5, ...)
    ],
    error_threshold_percent=10.0,
    tags=["8086", "emulator"]
)
```

### 4. Validation Engine

Runs cases and generates reports:

```python
engine = ValidationEngine(model_interface)
report = engine.run_validation()
engine.print_report(report)
```

---

## Usage

### Basic Validation Run

```python
from validation_framework import ValidationEngine
from pre1986_unified import ModelingInterface

# Initialize
model = ModelingInterface()
engine = ValidationEngine(model)

# Run all validation cases
report = engine.run_validation()

# Print report
engine.print_report(report)

# Export
engine.export_report(report, "validation_results.json")
```

### Filter by Processor

```python
# Validate only Intel processors
report = engine.run_validation(processors=["Intel 8086", "Intel 8080"])
```

### Filter by Tags

```python
# Validate only emulator-based cases
report = engine.run_validation(tags=["emulator"])

# Validate only datasheet timing cases
report = engine.run_validation(tags=["datasheet", "timing"])
```

### Add Custom Validation Case

```python
from validation_framework import (
    ValidationCaseBuilder, 
    ValidationSource, 
    DataSource
)

# Define source
my_source = ValidationSource(
    name="My Lab Measurement",
    source_type=DataSource.HARDWARE,
    description="Measured on original 8086 hardware",
    reliability_score=0.90
)

# Build case using fluent builder
case = (ValidationCaseBuilder("my_8086_test")
    .processor("Intel 8086")
    .description("Custom measurement from my lab")
    .workload("compute")
    .clock(4.77)
    .measured_ipc(0.12, source=my_source, uncertainty=0.01)
    .measured_cpi(8.3, source=my_source)
    .threshold(15.0)
    .tags(["custom", "8086", "hardware"])
    .build())

# Add to repository
engine.repository.add_case(case)

# Run
report = engine.run_validation(cases=[case])
```

---

## Validation Report Structure

```
======================================================================
  VALIDATION REPORT
======================================================================
  Timestamp: 2026-01-25T19:17:59

  ┌─ SUMMARY ────────────────────────────────────────────────────────┐
  │  Total: 15  |  Passed: 10  |  Failed: 3  |  Warnings: 1  |  Skipped: 1  │
  │  Pass Rate: 71.4%                                                    │
  └──────────────────────────────────────────────────────────────────┘

  ┌─ ERROR STATISTICS ───────────────────────────────────────────────┐
  │  Mean Error:     5.23%                                              │
  │  Median Error:   4.15%                                              │
  │  Best Case:    8086_datasheet_timing  (1.2%)                       │
  │  Worst Case:   68000_amiga_dhrystone  (18.5%)                      │
  └──────────────────────────────────────────────────────────────────┘

  ┌─ BY PROCESSOR ───────────────────────────────────────────────────┐
  │  Processor                   Pass   Fail    Error                   │
  │  Intel 8086                     3      0    2.50%                   │
  │  MOS 6502                       2      1    5.30%                   │
  │  Zilog Z80                      2      0    3.80%                   │
  │  Motorola 68000                 1      2   12.40%                   │
  └──────────────────────────────────────────────────────────────────┘

  ┌─ DETAILED RESULTS ───────────────────────────────────────────────┐
  │  Case ID                        Status        Error                  │
  │  ✓ 8086_datasheet_timing        passed        1.20%                  │
  │  ✓ 8086_ea_timing               passed        2.80%                  │
  │  ✗ 68000_amiga_dhrystone        failed       18.50%                  │
  │  ⚠ 6502_sieve                   warning       9.80%                  │
  └──────────────────────────────────────────────────────────────────┘
```

---

## Built-in Validation Cases

### By Processor

| Processor | Cases | Coverage |
|-----------|-------|----------|
| Intel 8080 | 2 | Datasheet timing, BYTE Sieve |
| Intel 8086 | 4 | Datasheet, EA timing, MAME, Dhrystone |
| MOS 6502 | 3 | Datasheet, VICE, Apple II Sieve |
| Zilog Z80 | 2 | Datasheet, LDIR block timing |
| Motorola 68000 | 3 | Datasheet, Hatari, Amiga Dhrystone |
| Intel 80386 | 1 | Datasheet timing |

### By Source Type

| Source | Cases | Notes |
|--------|-------|-------|
| Datasheets | 7 | Highest reliability |
| Emulators | 4 | MAME, VICE, Hatari |
| Benchmarks | 4 | Dhrystone, BYTE Sieve |

---

## Error Thresholds

Default thresholds by case type:

| Case Type | Threshold | Rationale |
|-----------|-----------|-----------|
| Datasheet timing | 5% | Should match exactly |
| Emulator cycles | 10% | Good accuracy expected |
| Benchmark results | 15-20% | Compiler/system variation |
| Hardware measurement | 10-15% | Measurement uncertainty |

---

## Extending the Framework

### Adding New Validation Sources

```python
engine.repository.add_source(ValidationSource(
    name="My Emulator",
    source_type=DataSource.EMULATOR,
    description="Custom cycle-accurate emulator",
    reliability_score=0.85
))
```

### Adding Cases from CSV

```python
def load_cases_from_csv(filename: str, engine: ValidationEngine):
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            case = (ValidationCaseBuilder(row['id'])
                .processor(row['processor'])
                .description(row['description'])
                .measured_cpi(float(row['cpi']))
                .threshold(float(row['threshold']))
                .build())
            engine.repository.add_case(case)
```

### Custom Validation Logic

```python
class CustomValidationEngine(ValidationEngine):
    def _calculate_error(self, predicted, measured):
        # Custom error calculation
        # e.g., weighted by uncertainty
        pass
    
    def _run_single_case(self, case):
        # Custom case execution logic
        pass
```

---

## Workflow for Model Improvement

```
┌─────────────────┐
│  1. Run         │
│  Validation     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│  2. Identify    │────▶│  3. Investigate │
│  Failed Cases   │     │  Root Cause     │
└─────────────────┘     └────────┬────────┘
                                 │
         ┌───────────────────────┘
         ▼
┌─────────────────┐     ┌─────────────────┐
│  4. Update      │────▶│  5. Re-run      │
│  Model          │     │  Validation     │
└─────────────────┘     └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │  6. Track       │
                        │  Improvement    │
                        └─────────────────┘
```

---

## Files

| File | Description |
|------|-------------|
| `validation_framework.py` | Core framework |
| `VALIDATION_README.md` | This documentation |

---

## Future Enhancements

- [ ] Load validation data from YAML/JSON files
- [ ] Automatic data collection from emulators
- [ ] Regression tracking over time
- [ ] Web dashboard for results
- [ ] Integration with CI/CD pipelines

---

**Framework Version:** 1.0  
**Last Updated:** January 25, 2026
