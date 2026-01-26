# MOS 6502 Performance Model

Grey-box queueing model for the MOS 6502 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1975 |
| Clock | 1.0 MHz |
| Bus Width | 8-bit |
| Transistors | 3,510 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| implied | 2 | 0.18 | TAX, INX, etc. |
| immediate | 2 | 0.18 | LDA #imm |
| zero_page | 3 | 0.22 | LDA $00 |
| zero_page_x | 4 | 0.10 | LDA $00,X |
| absolute | 4 | 0.10 | LDA $0000 |
| absolute_x | 5 | 0.05 | LDA $0000,X (+1 page) |
| branch_taken | 3 | 0.08 | BNE taken |
| branch_not_taken | 2 | 0.04 | BNE not taken |
| jsr_rts | 6 | 0.05 | JSR=6, RTS=6 |


## Performance Targets

- **IPS Range**: 430,000 - 1,000,000
- **CPI Range**: 2 - 7
- **Primary Bottleneck**: memory, fetch

## Usage

```python
from mos6502_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

MOS 6500 Hardware Manual
