# Novix NC4016 Performance Model

Grey-box queueing model for the Novix NC4016 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1985 |
| Clock | 8.0 MHz |
| Bus Width | 16-bit |
| Transistors | 12,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| alu | 1 | 0.40 | ALU operations |
| stack | 1 | 0.25 | Stack operations |
| memory | 2 | 0.12 | Memory access |
| call_ret | 1 | 0.10 | CALL, RET |
| branch | 2 | 0.08 | Branch |
| misc | 1 | 0.05 | Other |


## Performance Targets

- **IPS Range**: 6,000,000 - 10,000,000
- **CPI Range**: 1 - 2
- **Primary Bottleneck**: stack, memory

## Usage

```python
from nc4016_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

Novix NC4016 Data Sheet
