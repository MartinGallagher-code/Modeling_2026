# National NS32032 Performance Model

Grey-box queueing model for the National NS32032 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1984 |
| Clock | 15.0 MHz |
| Bus Width | 32-bit |
| Transistors | 80,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| mov_reg | 4 | 0.25 | MOV reg,reg |
| mov_mem | 8 | 0.18 | MOV mem,reg |
| alu_reg | 4 | 0.25 | ALU reg,reg |
| alu_mem | 10 | 0.10 | ALU mem,reg |
| branch | 6 | 0.08 | Branch |
| call_ret | 15 | 0.06 | BSR, RET |
| multiply | 18 | 0.04 | MUL |
| divide | 35 | 0.02 | DIV |
| misc | 4 | 0.02 | Other |


## Performance Targets

- **IPS Range**: 1,500,000 - 4,000,000
- **CPI Range**: 4 - 20
- **Primary Bottleneck**: decode, memory

## Usage

```python
from ns32032_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

NS32032 Data Sheet
