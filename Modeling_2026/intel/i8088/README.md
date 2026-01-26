# Intel 8088 Performance Model

Grey-box queueing model for the Intel 8088 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1979 |
| Clock | 5.0 MHz |
| Bus Width | 8-bit |
| Transistors | 29,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| mov_reg_reg | 2 | 0.18 | MOV r,r |
| mov_reg_mem | 16 | 0.15 | MOV r,m (slower bus) |
| alu_register | 3 | 0.20 | ADD/SUB/AND/OR r,r |
| alu_memory | 21 | 0.10 | ALU with memory |
| immediate | 4 | 0.12 | MOV r,imm |
| branch_taken | 16 | 0.08 | Jcc taken |
| branch_not_taken | 4 | 0.05 | Jcc not taken |
| call_return | 28 | 0.05 | CALL near |
| string_ops | 22 | 0.04 | String operations |
| multiply | 143 | 0.03 | MUL/IMUL |


## Performance Targets

- **IPS Range**: 250,000 - 500,000
- **CPI Range**: 10 - 20
- **Primary Bottleneck**: prefetch, bus_width

## Usage

```python
from i8088_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

Intel 8088 Users Manual
