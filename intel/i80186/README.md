# Intel 80186 Performance Model

Grey-box queueing model for the Intel 80186 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1982 |
| Clock | 8.0 MHz |
| Bus Width | 16-bit |
| Transistors | 55,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| mov_reg_reg | 2 | 0.20 | MOV r,r |
| mov_reg_mem | 9 | 0.15 | MOV r,m |
| alu_register | 3 | 0.22 | ALU r,r |
| alu_memory | 12 | 0.10 | ALU r,m |
| immediate | 3 | 0.12 | Immediate ops |
| branch_taken | 13 | 0.08 | Jcc taken |
| branch_not_taken | 4 | 0.05 | Jcc not taken |
| call_return | 15 | 0.05 | CALL/RET |
| multiply | 36 | 0.03 | MUL/IMUL (faster) |


## Performance Targets

- **IPS Range**: 900,000 - 1,500,000
- **CPI Range**: 5 - 10
- **Primary Bottleneck**: decode, memory

## Usage

```python
from i80186_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

Intel 80186/80188 Users Manual
