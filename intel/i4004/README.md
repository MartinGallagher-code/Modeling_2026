# Intel 4004 Performance Model

Grey-box queueing model for the Intel 4004 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1971 |
| Clock | 0.74 MHz |
| Bus Width | 4-bit |
| Transistors | 2,300 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| register_ops | 8 | 0.25 | INC, ADD, SUB, LD, XCH |
| accumulator_imm | 16 | 0.15 | LDM, FIM |
| memory_ops | 8 | 0.20 | RDM, WRM, RDR, WRR |
| bcd_arithmetic | 8 | 0.10 | DAA, CLC, STC |
| jump_unconditional | 16 | 0.08 | JUN |
| jump_conditional | 16 | 0.07 | JCN |
| subroutine | 16 | 0.05 | JMS, BBL |
| io_ops | 8 | 0.08 | I/O operations |
| nop_misc | 8 | 0.02 | NOP |


## Performance Targets

- **IPS Range**: 46,000 - 93,000
- **CPI Range**: 8 - 16
- **Primary Bottleneck**: fetch, sequential fetch

## Usage

```python
from i4004_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

MCS-4 Users Manual
