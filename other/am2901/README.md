# AMD Am2901 Performance Model

Grey-box queueing model for the AMD Am2901 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1975 |
| Clock | 10.0 MHz |
| Bus Width | 4-bit |
| Transistors | 1,700 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| alu_pass | 1 | 0.30 | ALU pass through |
| alu_add | 1 | 0.25 | ALU add |
| alu_sub | 1 | 0.15 | ALU subtract |
| alu_logic | 1 | 0.15 | ALU logic ops |
| shift | 2 | 0.08 | Shift operations |
| ram_access | 1 | 0.05 | RAM access |
| output | 1 | 0.02 | Output |


## Performance Targets

- **IPS Range**: 2,000,000 - 10,000,000
- **CPI Range**: 1 - 5
- **Primary Bottleneck**: microcode, external

## Usage

```python
from am2901_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

AMD Am2901 Data Sheet
