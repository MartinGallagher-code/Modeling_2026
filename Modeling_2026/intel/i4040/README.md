# Intel 4040 Performance Model

Grey-box queueing model for the Intel 4040 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1974 |
| Clock | 0.74 MHz |
| Bus Width | 4-bit |
| Transistors | 3,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| register_ops | 8 | 0.25 | INC, ADD, SUB, LD, XCH |
| accumulator_imm | 16 | 0.15 | LDM, FIM |
| memory_ops | 8 | 0.18 | RDM, WRM |
| bcd_arithmetic | 8 | 0.10 | DAA operations |
| jump_unconditional | 16 | 0.08 | JUN |
| jump_conditional | 16 | 0.07 | JCN |
| subroutine | 16 | 0.05 | JMS, BBL |
| io_ops | 8 | 0.08 | I/O operations |
| interrupt | 16 | 0.02 | Interrupt handling |
| nop_misc | 8 | 0.02 | NOP, HLT |


## Performance Targets

- **IPS Range**: 50,000 - 100,000
- **CPI Range**: 7 - 15
- **Primary Bottleneck**: fetch, sequential fetch

## Usage

```python
from i4040_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

MCS-40 Users Manual
