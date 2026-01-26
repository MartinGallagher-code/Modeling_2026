# Intel 8008 Performance Model

Grey-box queueing model for the Intel 8008 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1972 |
| Clock | 0.5 MHz |
| Bus Width | 8-bit |
| Transistors | 3,500 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| mov_reg_reg | 10 | 0.20 | MOV r1,r2 (5 T-states) |
| mov_reg_mem | 16 | 0.15 | MOV r,M / MOV M,r |
| alu_register | 10 | 0.20 | ADD/SUB/AND/OR r |
| alu_memory | 16 | 0.10 | ADD M, etc. |
| immediate | 16 | 0.10 | MVI, ADI, etc. |
| jump_unconditional | 22 | 0.08 | JMP |
| jump_conditional | 18 | 0.07 | Jcc |
| call_return | 22 | 0.05 | CALL, RET |
| io_ops | 16 | 0.03 | IN, OUT |
| misc | 10 | 0.02 | HLT, NOP |


## Performance Targets

- **IPS Range**: 23,000 - 80,000
- **CPI Range**: 10 - 22
- **Primary Bottleneck**: fetch, sequential

## Usage

```python
from i8008_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

Intel 8008 Users Manual
