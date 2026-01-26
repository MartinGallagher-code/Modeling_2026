# Intel 80287 Performance Model

Grey-box queueing model for the Intel 80287 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1982 |
| Clock | 8.0 MHz |
| Bus Width | 16-bit |
| Transistors | 45,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| fld | 40 | 0.20 | FLD (load) |
| fst | 50 | 0.15 | FST (store) |
| fadd | 90 | 0.20 | FADD |
| fsub | 90 | 0.10 | FSUB |
| fmul | 140 | 0.15 | FMUL |
| fdiv | 200 | 0.10 | FDIV |
| fsqrt | 180 | 0.05 | FSQRT |
| fcomp | 50 | 0.05 | FCOMP |


## Performance Targets

- **IPS Range**: 50,000 - 150,000
- **CPI Range**: 50 - 200
- **Primary Bottleneck**: execute, fpu

## Usage

```python
from i80287_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

Intel 80287 Programmers Reference
