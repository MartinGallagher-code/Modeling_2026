# Motorola 6802 Performance Model

Grey-box queueing model for the Motorola 6802 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1977 |
| Clock | 1.0 MHz |
| Bus Width | 8-bit |
| Transistors | 5,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| inherent | 2 | 0.20 | Inherent addressing |
| immediate | 2 | 0.18 | Immediate |
| direct | 3 | 0.20 | Direct page |
| extended | 4 | 0.12 | Extended |
| indexed | 5 | 0.10 | Indexed |
| branch_taken | 4 | 0.08 | Branch taken |
| branch_not_taken | 4 | 0.05 | Branch not taken |
| jsr_rts | 9 | 0.05 | JSR, RTS |
| stack | 4 | 0.02 | Stack ops |


## Performance Targets

- **IPS Range**: 250,000 - 500,000
- **CPI Range**: 2 - 10
- **Primary Bottleneck**: memory, fetch

## Usage

```python
from m6802_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

Motorola MC6802 Data Sheet
