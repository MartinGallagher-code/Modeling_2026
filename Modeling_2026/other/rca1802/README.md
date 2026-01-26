# RCA 1802 Performance Model

Grey-box queueing model for the RCA 1802 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1976 |
| Clock | 2.0 MHz |
| Bus Width | 8-bit |
| Transistors | 5,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| short_branch | 8 | 0.15 | Short branch |
| long_branch | 16 | 0.08 | Long branch |
| memory_ref | 8 | 0.20 | Memory reference |
| reg_ops | 8 | 0.25 | Register ops |
| immediate | 16 | 0.12 | Immediate |
| io_ops | 8 | 0.10 | I/O operations |
| control | 8 | 0.05 | Control |
| subroutine | 24 | 0.05 | SEP, RET |


## Performance Targets

- **IPS Range**: 125,000 - 400,000
- **CPI Range**: 8 - 24
- **Primary Bottleneck**: fetch, decode

## Usage

```python
from rca1802_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

RCA CDP1802 Users Manual
