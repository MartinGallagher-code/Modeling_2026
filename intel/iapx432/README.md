# Intel iAPX 432 Performance Model

Grey-box queueing model for the Intel iAPX 432 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1981 |
| Clock | 8.0 MHz |
| Bus Width | 32-bit |
| Transistors | 220,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| simple_ops | 20 | 0.25 | Simple operations |
| memory_ops | 30 | 0.20 | Memory access |
| object_ops | 50 | 0.15 | Object manipulation |
| branch | 35 | 0.12 | Branch operations |
| call_return | 80 | 0.10 | Procedure call |
| capability | 100 | 0.10 | Capability operations |
| context_switch | 200 | 0.05 | Context switch |
| misc | 25 | 0.03 | Other |


## Performance Targets

- **IPS Range**: 100,000 - 300,000
- **CPI Range**: 25 - 80
- **Primary Bottleneck**: decode, microcode

## Usage

```python
from iapx432_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

Intel iAPX 432 General Data Processor
