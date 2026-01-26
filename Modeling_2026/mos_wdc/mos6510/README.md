# MOS 6510 Performance Model

Grey-box queueing model for the MOS 6510 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1982 |
| Clock | 1.0 MHz |
| Bus Width | 8-bit |
| Transistors | 4,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| implied | 2 | 0.18 | Implied |
| immediate | 2 | 0.18 | Immediate |
| zero_page | 3 | 0.22 | Zero page |
| zero_page_x | 4 | 0.10 | Zero page,X |
| absolute | 4 | 0.10 | Absolute |
| absolute_x | 5 | 0.05 | Absolute,X |
| branch_taken | 3 | 0.08 | Branch taken |
| branch_not_taken | 2 | 0.04 | Branch not taken |
| jsr_rts | 6 | 0.05 | JSR, RTS |


## Performance Targets

- **IPS Range**: 430,000 - 1,000,000
- **CPI Range**: 2 - 7
- **Primary Bottleneck**: memory, fetch

## Usage

```python
from mos6510_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

MOS 6510 Data Sheet
