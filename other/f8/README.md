# Fairchild F8 Performance Model

Grey-box queueing model for the Fairchild F8 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1975 |
| Clock | 2.0 MHz |
| Bus Width | 8-bit |
| Transistors | 4,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| accumulator | 4 | 0.25 | Accumulator ops |
| scratchpad | 4 | 0.20 | Scratchpad |
| memory | 8 | 0.15 | Memory |
| immediate | 5 | 0.15 | Immediate |
| branch | 8 | 0.10 | Branch |
| call_return | 13 | 0.08 | PI, POP |
| io | 8 | 0.05 | I/O |
| misc | 4 | 0.02 | Other |


## Performance Targets

- **IPS Range**: 200,000 - 500,000
- **CPI Range**: 4 - 13
- **Primary Bottleneck**: fetch, decode

## Usage

```python
from f8_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

Fairchild F8 Users Guide
