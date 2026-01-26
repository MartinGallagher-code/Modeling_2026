# Harris RTX2000 Performance Model

Grey-box queueing model for the Harris RTX2000 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1988 |
| Clock | 10.0 MHz |
| Bus Width | 16-bit |
| Transistors | 15,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| alu | 1 | 0.40 | ALU operations |
| stack | 1 | 0.20 | Stack operations |
| memory | 2 | 0.15 | Memory access |
| call_ret | 1 | 0.10 | CALL, RET |
| branch | 2 | 0.08 | Branch |
| multiply | 2 | 0.05 | Multiply |
| misc | 1 | 0.02 | Other |


## Performance Targets

- **IPS Range**: 8,000,000 - 12,000,000
- **CPI Range**: 1 - 2
- **Primary Bottleneck**: stack, memory

## Usage

```python
from rtx2000_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

Harris RTX2000 Data Sheet
