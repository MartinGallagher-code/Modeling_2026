# Motorola 68882 Performance Model

Grey-box queueing model for the Motorola 68882 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1985 |
| Clock | 25.0 MHz |
| Bus Width | 32-bit |
| Transistors | 175,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| fmove | 15 | 0.20 | FMOVE |
| fadd | 25 | 0.20 | FADD |
| fsub | 25 | 0.10 | FSUB |
| fmul | 35 | 0.20 | FMUL |
| fdiv | 75 | 0.10 | FDIV |
| fsqrt | 100 | 0.05 | FSQRT |
| fsin_fcos | 160 | 0.05 | FSIN, FCOS |
| fcomp | 20 | 0.10 | FCMP |


## Performance Targets

- **IPS Range**: 250,000 - 800,000
- **CPI Range**: 25 - 100
- **Primary Bottleneck**: execute, fpu

## Usage

```python
from m68882_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

MC68882 Users Manual
