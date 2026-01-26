# Motorola 68881 Performance Model

Grey-box queueing model for the Motorola 68881 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1984 |
| Clock | 16.0 MHz |
| Bus Width | 32-bit |
| Transistors | 155,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| fmove | 20 | 0.20 | FMOVE |
| fadd | 30 | 0.20 | FADD |
| fsub | 30 | 0.10 | FSUB |
| fmul | 45 | 0.20 | FMUL |
| fdiv | 90 | 0.10 | FDIV |
| fsqrt | 120 | 0.05 | FSQRT |
| fsin_fcos | 200 | 0.05 | FSIN, FCOS |
| fcomp | 25 | 0.10 | FCMP |


## Performance Targets

- **IPS Range**: 150,000 - 500,000
- **CPI Range**: 30 - 120
- **Primary Bottleneck**: execute, fpu

## Usage

```python
from m68881_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

MC68881 Users Manual
