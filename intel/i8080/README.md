# Intel 8080 Performance Model

Grey-box queueing model for the Intel 8080 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1974 |
| Clock | 2.0 MHz |
| Bus Width | 8-bit |
| Transistors | 4,500 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| mov_reg_reg | 5 | 0.20 | MOV r1,r2 |
| mov_reg_mem | 7 | 0.15 | MOV r,M / MOV M,r |
| alu_register | 4 | 0.25 | ADD/SUB/AND/OR r |
| alu_memory | 7 | 0.10 | ADD M, etc. |
| immediate | 7 | 0.10 | MVI, ADI, etc. |
| branch_taken | 10 | 0.08 | JZ, JNZ taken |
| branch_not_taken | 10 | 0.04 | Jcc not taken |
| call_return | 17 | 0.05 | CALL=17, RET=10 |
| stack_ops | 11 | 0.03 | PUSH/POP |


## Performance Targets

- **IPS Range**: 290,000 - 500,000
- **CPI Range**: 4 - 18
- **Primary Bottleneck**: decode, fetch

## Usage

```python
from i8080_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

Intel 8080 Microcomputer Systems User Manual
