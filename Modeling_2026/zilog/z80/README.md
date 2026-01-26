# Zilog Z80 Performance Model

Grey-box queueing model for the Zilog Z80 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1976 |
| Clock | 2.5 MHz |
| Bus Width | 8-bit |
| Transistors | 8,500 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| ld_r_r | 4 | 0.20 | LD r,r |
| ld_r_n | 7 | 0.12 | LD r,n |
| ld_r_hl | 7 | 0.15 | LD r,(HL) |
| ld_r_ix | 19 | 0.05 | LD r,(IX+d) |
| alu_r | 4 | 0.18 | ADD, SUB, etc. |
| alu_hl | 7 | 0.08 | ADD A,(HL) |
| jp | 10 | 0.08 | JP nn |
| jr_taken | 12 | 0.05 | JR cc taken |
| jr_not_taken | 7 | 0.03 | JR cc not taken |
| call_ret | 17 | 0.04 | CALL, RET |
| push_pop | 11 | 0.02 | PUSH, POP |


## Performance Targets

- **IPS Range**: 290,000 - 800,000
- **CPI Range**: 4 - 23
- **Primary Bottleneck**: decode, fetch

## Usage

```python
from z80_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

Z80 CPU Users Manual
