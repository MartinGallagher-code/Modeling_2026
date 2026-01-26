# National NS32016 Performance Model

Grey-box queueing model for the National NS32016 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1982 |
| Clock | 10.0 MHz |
| Bus Width | 16-bit |
| Transistors | 60,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| mov_reg | 5 | 0.22 | MOV reg,reg |
| mov_mem | 12 | 0.18 | MOV mem,reg |
| alu_reg | 5 | 0.22 | ALU reg,reg |
| alu_mem | 14 | 0.10 | ALU mem,reg |
| branch | 8 | 0.10 | Branch |
| call_ret | 20 | 0.06 | BSR, RET |
| multiply | 25 | 0.05 | MUL |
| divide | 50 | 0.02 | DIV |
| misc | 5 | 0.05 | Other |


## Performance Targets

- **IPS Range**: 800,000 - 2,000,000
- **CPI Range**: 5 - 25
- **Primary Bottleneck**: decode, memory

## Usage

```python
from ns32016_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

NS32016 Data Sheet
