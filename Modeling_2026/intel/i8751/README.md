# Intel 8751 Performance Model

Grey-box queueing model for the Intel 8751 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1980 |
| Clock | 12.0 MHz |
| Bus Width | 8-bit |
| Transistors | 128,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| mov_direct | 12 | 0.20 | MOV direct |
| mov_indirect | 12 | 0.15 | MOV @Ri |
| alu_ops | 12 | 0.25 | ALU operations |
| immediate | 12 | 0.12 | MOV #data |
| branch | 24 | 0.10 | Branch ops |
| call_return | 24 | 0.05 | CALL, RET |
| bit_ops | 12 | 0.08 | Bit operations |
| multiply | 48 | 0.03 | MUL, DIV |
| misc | 12 | 0.02 | NOP |


## Performance Targets

- **IPS Range**: 500,000 - 1,000,000
- **CPI Range**: 12 - 24
- **Primary Bottleneck**: decode, memory

## Usage

```python
from i8751_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

Intel MCS-51 Users Manual
