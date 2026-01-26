# MIPS R2000 Performance Model

Grey-box queueing model for the MIPS R2000 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1985 |
| Clock | 8.0 MHz |
| Bus Width | 32-bit |
| Transistors | 110,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| alu_reg | 1 | 0.30 | ALU R-type |
| load | 2 | 0.20 | LW (load delay) |
| store | 1 | 0.12 | SW |
| branch | 1 | 0.12 | BEQ, BNE (delay slot) |
| jump | 1 | 0.08 | J, JAL |
| immediate | 1 | 0.10 | ADDI, ORI, etc. |
| multiply | 12 | 0.05 | MULT |
| divide | 35 | 0.03 | DIV |


## Performance Targets

- **IPS Range**: 5,000,000 - 10,000,000
- **CPI Range**: 1 - 3
- **Primary Bottleneck**: pipeline, cache

## Usage

```python
from r2000_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

MIPS R2000 Users Manual
