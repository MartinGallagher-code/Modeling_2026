# Intel 80386 Performance Model

Grey-box queueing model for the Intel 80386 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1985 |
| Clock | 16.0 MHz |
| Bus Width | 32-bit |
| Transistors | 275,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| mov_reg_reg | 2 | 0.22 | MOV r,r |
| mov_reg_mem | 4 | 0.18 | MOV r,m |
| alu_register | 2 | 0.25 | ALU r,r |
| alu_memory | 6 | 0.10 | ALU r,m |
| immediate | 2 | 0.10 | Immediate ops |
| branch_taken | 10 | 0.06 | Jcc taken |
| branch_not_taken | 3 | 0.04 | Jcc not taken |
| call_return | 10 | 0.03 | CALL/RET |
| multiply | 14 | 0.02 | MUL/IMUL |


## Performance Targets

- **IPS Range**: 3,000,000 - 11,000,000
- **CPI Range**: 2 - 6
- **Primary Bottleneck**: cache, memory

## Usage

```python
from i80386_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

Intel 80386 Programmers Reference Manual
