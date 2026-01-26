# TI TMS320C10 Performance Model

Grey-box queueing model for the TI TMS320C10 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1983 |
| Clock | 20.0 MHz |
| Bus Width | 16-bit |
| Transistors | 15,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| accumulator | 1 | 0.30 | Accumulator ops |
| mac | 1 | 0.25 | MAC (multiply-accumulate) |
| load_store | 1 | 0.15 | Load/Store |
| branch | 2 | 0.10 | Branch |
| call_ret | 2 | 0.08 | CALL, RET |
| io | 2 | 0.07 | I/O |
| misc | 1 | 0.05 | Other |


## Performance Targets

- **IPS Range**: 5,000,000 - 10,000,000
- **CPI Range**: 1 - 4
- **Primary Bottleneck**: memory, pipeline

## Usage

```python
from tms320c10_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

TI TMS320C1x Users Guide
