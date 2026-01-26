# Intel 80188 Performance Model

Grey-box queueing model for the Intel 80188 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1982 |
| Clock | 8.0 MHz |
| Bus Width | 8-bit |
| Transistors | 55,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| mov_reg_reg | 2 | 0.20 | MOV r,r |
| mov_reg_mem | 12 | 0.15 | MOV r,m |
| alu_register | 3 | 0.22 | ALU r,r |
| alu_memory | 16 | 0.10 | ALU r,m |
| immediate | 3 | 0.12 | Immediate ops |
| branch_taken | 13 | 0.08 | Jcc taken |
| branch_not_taken | 4 | 0.05 | Jcc not taken |
| call_return | 18 | 0.05 | CALL/RET |
| multiply | 40 | 0.03 | MUL/IMUL |


## Performance Targets

- **IPS Range**: 700,000 - 1,200,000
- **CPI Range**: 7 - 12
- **Primary Bottleneck**: prefetch, bus_width

## Usage

```python
from i80188_model import analyze, validate

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
