# Zilog Z8 Performance Model

Grey-box queueing model for the Zilog Z8 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1979 |
| Clock | 8.0 MHz |
| Bus Width | 8-bit |
| Transistors | 9,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| ld_r_r | 6 | 0.22 | LD r,r |
| ld_r_im | 6 | 0.15 | LD r,#imm |
| ld_r_ir | 8 | 0.15 | LD r,@Rr |
| alu_r | 6 | 0.20 | ALU r,r |
| jp | 10 | 0.10 | JP cc |
| call_ret | 14 | 0.08 | CALL, RET |
| djnz | 12 | 0.05 | DJNZ |
| misc | 6 | 0.05 | Other |


## Performance Targets

- **IPS Range**: 500,000 - 1,000,000
- **CPI Range**: 6 - 20
- **Primary Bottleneck**: decode, memory

## Usage

```python
from z8_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

Z8 MCU Users Manual
