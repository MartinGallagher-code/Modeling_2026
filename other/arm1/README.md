# Acorn ARM1 Performance Model

Grey-box queueing model for the Acorn ARM1 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1985 |
| Clock | 8.0 MHz |
| Bus Width | 32-bit |
| Transistors | 25,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| data_proc | 1 | 0.35 | Data processing |
| load_single | 3 | 0.18 | LDR |
| store_single | 2 | 0.10 | STR |
| load_multiple | 4 | 0.05 | LDM |
| branch | 3 | 0.12 | B, BL |
| branch_link | 4 | 0.05 | BL |
| multiply | 16 | 0.05 | MUL |
| swi | 4 | 0.02 | SWI |
| misc | 1 | 0.08 | Other |


## Performance Targets

- **IPS Range**: 4,000,000 - 8,000,000
- **CPI Range**: 1 - 4
- **Primary Bottleneck**: memory, pipeline

## Usage

```python
from arm1_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

ARM1 Technical Reference Manual
