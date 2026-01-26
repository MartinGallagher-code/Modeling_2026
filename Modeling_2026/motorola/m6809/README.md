# Motorola 6809 Performance Model

Grey-box queueing model for the Motorola 6809 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1978 |
| Clock | 1.0 MHz |
| Bus Width | 8-bit |
| Transistors | 9,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| inherent | 2 | 0.18 | Inherent |
| immediate | 2 | 0.18 | Immediate |
| direct | 4 | 0.18 | Direct |
| indexed | 5 | 0.15 | Indexed |
| extended | 5 | 0.10 | Extended |
| branch_short | 3 | 0.08 | Short branch |
| branch_long | 5 | 0.05 | Long branch |
| jsr_rts | 7 | 0.05 | JSR, RTS |
| multiply | 11 | 0.03 | MUL |


## Performance Targets

- **IPS Range**: 250,000 - 600,000
- **CPI Range**: 2 - 8
- **Primary Bottleneck**: memory, fetch

## Usage

```python
from m6809_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

Motorola MC6809 Programming Manual
