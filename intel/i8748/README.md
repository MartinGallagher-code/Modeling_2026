# Intel 8748 Performance Model

Grey-box queueing model for the Intel 8748 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1977 |
| Clock | 6.0 MHz |
| Bus Width | 8-bit |
| Transistors | 8,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| mov_a_r | 15 | 0.25 | MOV A,Rn |
| mov_a_mem | 15 | 0.15 | MOV A,@Ri |
| alu_ops | 15 | 0.25 | ALU operations |
| immediate | 30 | 0.10 | MOV A,#data |
| jump | 30 | 0.10 | JMP, CALL |
| conditional | 30 | 0.08 | Conditional jumps |
| io_ops | 30 | 0.05 | I/O operations |
| misc | 15 | 0.02 | NOP |


## Performance Targets

- **IPS Range**: 400,000 - 750,000
- **CPI Range**: 8 - 15
- **Primary Bottleneck**: fetch

## Usage

```python
from i8748_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

Intel MCS-48 Users Manual
