# Intel 80286 Performance Model

Grey-box queueing model for the Intel 80286 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1982 |
| Clock | 8.0 MHz |
| Bus Width | 16-bit |
| Transistors | 134,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| mov_reg_reg | 2 | 0.22 | MOV r,r |
| mov_reg_mem | 5 | 0.15 | MOV r,m |
| alu_register | 2 | 0.25 | ALU r,r |
| alu_memory | 7 | 0.10 | ALU r,m |
| immediate | 3 | 0.10 | Immediate ops |
| branch_taken | 11 | 0.07 | Jcc taken |
| branch_not_taken | 3 | 0.04 | Jcc not taken |
| call_return | 13 | 0.05 | CALL/RET |
| multiply | 21 | 0.02 | MUL/IMUL |


## Performance Targets

- **IPS Range**: 900,000 - 2,700,000
- **CPI Range**: 3 - 9
- **Primary Bottleneck**: memory, decode

## Usage

```python
from i80286_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

Intel 80286 Programmers Reference Manual
