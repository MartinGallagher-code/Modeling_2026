# Motorola 68000 Performance Model

Grey-box queueing model for the Motorola 68000 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1979 |
| Clock | 8.0 MHz |
| Bus Width | 16-bit |
| Transistors | 68,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| move_reg | 4 | 0.20 | MOVE Dn,Dn |
| move_mem | 12 | 0.15 | MOVE (An),Dn |
| alu_reg | 4 | 0.20 | ADD, SUB, AND reg |
| alu_mem | 12 | 0.10 | ALU with memory |
| immediate | 8 | 0.10 | MOVE #imm |
| branch | 10 | 0.10 | Bcc |
| jsr_rts | 18 | 0.05 | JSR, RTS |
| multiply | 70 | 0.05 | MULS, MULU |
| divide | 158 | 0.03 | DIVS, DIVU |
| misc | 4 | 0.02 | NOP, etc. |


## Performance Targets

- **IPS Range**: 1,000,000 - 2,000,000
- **CPI Range**: 4 - 158
- **Primary Bottleneck**: ea_calc, decode

## Usage

```python
from m68000_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

M68000 Users Manual
