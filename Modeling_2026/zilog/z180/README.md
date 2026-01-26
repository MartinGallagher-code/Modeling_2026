# Zilog Z180 Performance Model

Grey-box queueing model for the Zilog Z180 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1985 |
| Clock | 6.0 MHz |
| Bus Width | 8-bit |
| Transistors | 20,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| ld_r_r | 3 | 0.22 | LD r,r |
| ld_r_n | 5 | 0.12 | LD r,n |
| ld_r_hl | 5 | 0.15 | LD r,(HL) |
| alu_r | 3 | 0.20 | ALU r |
| alu_hl | 5 | 0.08 | ALU (HL) |
| jp | 8 | 0.08 | JP |
| jr_taken | 10 | 0.05 | JR taken |
| call_ret | 14 | 0.05 | CALL, RET |
| multiply | 18 | 0.03 | MLT |
| push_pop | 9 | 0.02 | PUSH, POP |


## Performance Targets

- **IPS Range**: 900,000 - 2,000,000
- **CPI Range**: 3 - 18
- **Primary Bottleneck**: decode, memory

## Usage

```python
from z180_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

Z180 Users Manual
