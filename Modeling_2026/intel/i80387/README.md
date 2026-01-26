# Intel 80387 Performance Model

Grey-box queueing model for the Intel 80387 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1987 |
| Clock | 16.0 MHz |
| Bus Width | 32-bit |
| Transistors | 104,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| fld | 20 | 0.20 | FLD (load) |
| fst | 25 | 0.15 | FST (store) |
| fadd | 30 | 0.20 | FADD |
| fsub | 30 | 0.10 | FSUB |
| fmul | 50 | 0.15 | FMUL |
| fdiv | 90 | 0.10 | FDIV |
| fsqrt | 120 | 0.05 | FSQRT |
| fcomp | 25 | 0.05 | FCOMP |


## Performance Targets

- **IPS Range**: 150,000 - 500,000
- **CPI Range**: 30 - 120
- **Primary Bottleneck**: execute, fpu

## Usage

```python
from i80387_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

Intel 80387 Programmers Reference
