# Zilog Z8000 Performance Model

Grey-box queueing model for the Zilog Z8000 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1979 |
| Clock | 4.0 MHz |
| Bus Width | 16-bit |
| Transistors | 17,500 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| ld_r_r | 3 | 0.22 | LD R,R |
| ld_r_im | 4 | 0.15 | LD R,#imm |
| ld_r_mem | 7 | 0.18 | LD R,@addr |
| alu_r | 4 | 0.20 | ADD, SUB, etc. |
| alu_mem | 8 | 0.08 | ALU with memory |
| jp | 6 | 0.08 | JP cc |
| call_ret | 12 | 0.05 | CALL, RET |
| multiply | 70 | 0.02 | MULT |
| divide | 107 | 0.02 | DIV |


## Performance Targets

- **IPS Range**: 500,000 - 1,200,000
- **CPI Range**: 3 - 12
- **Primary Bottleneck**: decode, memory

## Usage

```python
from z8000_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

Z8000 CPU Users Manual
