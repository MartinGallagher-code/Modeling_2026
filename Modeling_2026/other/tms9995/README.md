# TI TMS9995 Performance Model

Grey-box queueing model for the TI TMS9995 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1981 |
| Clock | 12.0 MHz |
| Bus Width | 8-bit |
| Transistors | 24,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| register | 8 | 0.22 | Register-register |
| immediate | 10 | 0.15 | Immediate |
| memory | 16 | 0.18 | Memory |
| jump | 8 | 0.12 | Jump |
| cru | 10 | 0.08 | CRU bit ops |
| shift | 14 | 0.08 | Shift |
| multiply | 40 | 0.05 | MPY |
| divide | 60 | 0.02 | DIV |
| blwp | 18 | 0.05 | Context switch |
| misc | 8 | 0.05 | Other |


## Performance Targets

- **IPS Range**: 500,000 - 1,200,000
- **CPI Range**: 8 - 40
- **Primary Bottleneck**: memory, bus_width

## Usage

```python
from tms9995_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

TI TMS9995 Users Guide
