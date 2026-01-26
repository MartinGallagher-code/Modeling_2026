# AMD Am2903 Performance Model

Grey-box queueing model for the AMD Am2903 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1976 |
| Clock | 12.5 MHz |
| Bus Width | 4-bit |
| Transistors | 2,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| alu_pass | 1 | 0.28 | ALU pass through |
| alu_add | 1 | 0.25 | ALU add |
| alu_sub | 1 | 0.15 | ALU subtract |
| alu_logic | 1 | 0.15 | ALU logic ops |
| shift | 2 | 0.08 | Shift operations |
| multiply | 4 | 0.05 | Hardware multiply |
| ram_access | 1 | 0.04 | RAM access |


## Performance Targets

- **IPS Range**: 2,500,000 - 12,500,000
- **CPI Range**: 1 - 5
- **Primary Bottleneck**: microcode, external

## Usage

```python
from am2903_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

AMD Am2903 Data Sheet
