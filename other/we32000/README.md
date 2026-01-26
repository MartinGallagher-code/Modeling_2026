# AT&T WE 32000 Performance Model

Grey-box queueing model for the AT&T WE 32000 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1982 |
| Clock | 14.0 MHz |
| Bus Width | 32-bit |
| Transistors | 145,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| mov_reg | 4 | 0.22 | MOV reg,reg |
| mov_mem | 8 | 0.18 | MOV mem,reg |
| alu_reg | 4 | 0.22 | ALU reg,reg |
| alu_mem | 10 | 0.10 | ALU mem,reg |
| branch | 6 | 0.10 | Branch |
| call_ret | 12 | 0.06 | JSB, RSB |
| multiply | 15 | 0.05 | MULW |
| divide | 30 | 0.02 | DIVW |
| misc | 4 | 0.05 | Other |


## Performance Targets

- **IPS Range**: 1,000,000 - 3,000,000
- **CPI Range**: 4 - 15
- **Primary Bottleneck**: decode, memory

## Usage

```python
from we32000_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

WE 32000 Users Manual
