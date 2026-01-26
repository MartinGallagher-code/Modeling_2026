# Motorola 6801 Performance Model

Grey-box queueing model for the Motorola 6801 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1978 |
| Clock | 1.0 MHz |
| Bus Width | 8-bit |
| Transistors | 15,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| inherent | 2 | 0.20 | Inherent |
| immediate | 2 | 0.18 | Immediate |
| direct | 3 | 0.20 | Direct |
| indexed | 4 | 0.15 | Indexed |
| extended | 4 | 0.10 | Extended |
| branch | 3 | 0.08 | Branch |
| jsr_rts | 6 | 0.05 | JSR, RTS |
| multiply | 10 | 0.02 | MUL |
| misc | 2 | 0.02 | Other |


## Performance Targets

- **IPS Range**: 300,000 - 600,000
- **CPI Range**: 2 - 8
- **Primary Bottleneck**: memory, fetch

## Usage

```python
from m6801_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

MC6801 Data Sheet
