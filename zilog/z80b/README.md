# Zilog Z80B Performance Model

Grey-box queueing model for the Zilog Z80B microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1980 |
| Clock | 6.0 MHz |
| Bus Width | 8-bit |
| Transistors | 8,500 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| ld_r_r | 4 | 0.20 | LD r,r |
| ld_r_n | 7 | 0.12 | LD r,n |
| ld_r_hl | 7 | 0.15 | LD r,(HL) |
| ld_r_ix | 19 | 0.05 | LD r,(IX+d) |
| alu_r | 4 | 0.18 | ALU register |
| alu_hl | 7 | 0.08 | ALU (HL) |
| jp | 10 | 0.08 | JP |
| jr_taken | 12 | 0.05 | JR taken |
| jr_not_taken | 7 | 0.03 | JR not taken |
| call_ret | 17 | 0.04 | CALL, RET |
| push_pop | 11 | 0.02 | PUSH, POP |


## Performance Targets

- **IPS Range**: 690,000 - 1,920,000
- **CPI Range**: 4 - 23
- **Primary Bottleneck**: decode, memory

## Usage

```python
from z80b_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

Z80B Data Sheet
