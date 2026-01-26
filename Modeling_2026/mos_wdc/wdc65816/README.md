# WDC 65816 Performance Model

Grey-box queueing model for the WDC 65816 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1984 |
| Clock | 2.8 MHz |
| Bus Width | 16-bit |
| Transistors | 22,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| implied | 2 | 0.15 | Implied |
| immediate | 2 | 0.18 | Immediate |
| direct | 3 | 0.18 | Direct page |
| direct_x | 4 | 0.10 | Direct,X |
| absolute | 4 | 0.12 | Absolute |
| long | 5 | 0.08 | Long addressing |
| branch_taken | 3 | 0.08 | Branch taken |
| branch_not_taken | 2 | 0.04 | Branch not taken |
| jsr_rts | 8 | 0.07 | JSR, RTS |


## Performance Targets

- **IPS Range**: 1,000,000 - 2,500,000
- **CPI Range**: 2 - 8
- **Primary Bottleneck**: memory, fetch

## Usage

```python
from wdc65816_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

WDC 65816 Data Sheet
