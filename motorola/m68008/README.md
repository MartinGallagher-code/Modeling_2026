# Motorola 68008 Performance Model

Grey-box queueing model for the Motorola 68008 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1982 |
| Clock | 8.0 MHz |
| Bus Width | 8-bit |
| Transistors | 68,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| move_reg | 4 | 0.20 | MOVE Dn,Dn |
| move_mem | 18 | 0.15 | MOVE (An),Dn |
| alu_reg | 4 | 0.20 | ALU register |
| alu_mem | 18 | 0.10 | ALU memory |
| immediate | 12 | 0.10 | Immediate |
| branch | 14 | 0.10 | Branch |
| jsr_rts | 24 | 0.05 | JSR, RTS |
| multiply | 74 | 0.05 | Multiply |
| divide | 162 | 0.03 | Divide |
| misc | 4 | 0.02 | Other |


## Performance Targets

- **IPS Range**: 600,000 - 1,200,000
- **CPI Range**: 7 - 160
- **Primary Bottleneck**: bus_width, memory

## Usage

```python
from m68008_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

M68008 Users Manual
