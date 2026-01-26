# WDC 65C02 Performance Model

Grey-box queueing model for the WDC 65C02 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1983 |
| Clock | 2.0 MHz |
| Bus Width | 8-bit |
| Transistors | 4,500 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| implied | 2 | 0.18 | Implied |
| immediate | 2 | 0.18 | Immediate |
| zero_page | 3 | 0.22 | Zero page |
| zero_page_x | 4 | 0.10 | Zero page,X |
| absolute | 4 | 0.10 | Absolute |
| indirect_zp | 5 | 0.05 | (ZP) indirect |
| branch_taken | 3 | 0.08 | Branch taken |
| branch_not_taken | 2 | 0.04 | Branch not taken |
| jsr_rts | 6 | 0.05 | JSR, RTS |


## Performance Targets

- **IPS Range**: 900,000 - 2,000,000
- **CPI Range**: 2 - 6
- **Primary Bottleneck**: memory, fetch

## Usage

```python
from wdc65c02_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

WDC 65C02 Data Sheet
