# AMD Am29000 Performance Model

Grey-box queueing model for the AMD Am29000 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1987 |
| Clock | 25.0 MHz |
| Bus Width | 32-bit |
| Transistors | 300,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| alu_reg | 1 | 0.30 | ALU register |
| load | 2 | 0.18 | Load |
| store | 2 | 0.10 | Store |
| branch | 1 | 0.12 | Branch (delay slot) |
| call_ret | 4 | 0.08 | CALL, RET |
| multiply | 2 | 0.10 | Multiply |
| divide | 35 | 0.02 | Divide |
| misc | 1 | 0.10 | Other |


## Performance Targets

- **IPS Range**: 15,000,000 - 25,000,000
- **CPI Range**: 1 - 4
- **Primary Bottleneck**: cache, pipeline

## Usage

```python
from am29000_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

AMD Am29000 Users Manual
