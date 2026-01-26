# Intel 8085 Performance Model

Grey-box queueing model for the Intel 8085 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1976 |
| Clock | 3.0 MHz |
| Bus Width | 8-bit |
| Transistors | 6,500 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| mov_reg_reg | 4 | 0.22 | MOV r1,r2 |
| mov_reg_mem | 7 | 0.15 | MOV r,M |
| alu_register | 4 | 0.25 | ADD/SUB/AND/OR r |
| alu_memory | 7 | 0.08 | ADD M, etc. |
| immediate | 7 | 0.10 | MVI, ADI |
| branch_taken | 10 | 0.08 | Conditional jumps |
| branch_not_taken | 7 | 0.04 | Jcc not taken |
| call_return | 16 | 0.05 | CALL/RET |
| stack_ops | 12 | 0.03 | PUSH/POP |


## Performance Targets

- **IPS Range**: 370,000 - 770,000
- **CPI Range**: 4 - 16
- **Primary Bottleneck**: decode, memory

## Usage

```python
from i8085_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

Intel 8085A Users Manual
