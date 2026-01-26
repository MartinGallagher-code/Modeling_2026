# Intel 8086 Performance Model

Grey-box queueing model for the Intel 8086 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1978 |
| Clock | 5.0 MHz |
| Bus Width | 16-bit |
| Transistors | 29,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| mov_reg_reg | 2 | 0.18 | MOV r,r |
| mov_reg_mem | 12 | 0.15 | MOV r,m with EA calc |
| alu_register | 3 | 0.20 | ADD/SUB/AND/OR r,r |
| alu_memory | 17 | 0.10 | ALU with memory |
| immediate | 4 | 0.12 | MOV r,imm |
| branch_taken | 16 | 0.08 | Jcc taken |
| branch_not_taken | 4 | 0.05 | Jcc not taken |
| call_return | 23 | 0.05 | CALL near |
| string_ops | 18 | 0.04 | MOVSB, REP |
| multiply | 133 | 0.03 | MUL/IMUL |


## Performance Targets

- **IPS Range**: 330,000 - 750,000
- **CPI Range**: 7 - 15
- **Primary Bottleneck**: ea_calc, prefetch

## Usage

```python
from i8086_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

Intel 8086 Family Users Manual
