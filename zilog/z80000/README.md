# Zilog Z80000 Performance Model

Grey-box queueing model for the Zilog Z80000 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1986 |
| Clock | 25.0 MHz |
| Bus Width | 32-bit |
| Transistors | 91,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| ld_r_r | 2 | 0.25 | LD R,R |
| ld_r_mem | 4 | 0.20 | LD R,@addr |
| alu_r | 2 | 0.25 | ALU register |
| alu_mem | 5 | 0.10 | ALU memory |
| jp | 4 | 0.08 | JP |
| call_ret | 8 | 0.05 | CALL, RET |
| multiply | 15 | 0.04 | MULT |
| divide | 30 | 0.03 | DIV |


## Performance Targets

- **IPS Range**: 4,000,000 - 10,000,000
- **CPI Range**: 2 - 8
- **Primary Bottleneck**: cache, memory

## Usage

```python
from z80000_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

Z80000 CPU Manual
