# RCA 1805 Performance Model

Grey-box queueing model for the RCA 1805 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1977 |
| Clock | 3.0 MHz |
| Bus Width | 8-bit |
| Transistors | 6,000 |

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
| subroutine | 24 | 0.05 | Subroutine |


## Performance Targets

- **IPS Range**: 187,000 - 600,000
- **CPI Range**: 8 - 24
- **Primary Bottleneck**: fetch, decode

## Usage

```python
from rca1805_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

RCA CDP1805 Data Sheet
