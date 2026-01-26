# TI TMS9900 Performance Model

Grey-box queueing model for the TI TMS9900 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1976 |
| Clock | 3.0 MHz |
| Bus Width | 16-bit |
| Transistors | 8,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| register | 14 | 0.20 | Register-register |
| immediate | 14 | 0.15 | Immediate |
| memory | 22 | 0.18 | Memory |
| indexed | 26 | 0.10 | Indexed |
| jump | 10 | 0.12 | Jump |
| cru | 12 | 0.08 | CRU bit ops |
| shift | 20 | 0.05 | Shift |
| multiply | 52 | 0.05 | MPY |
| divide | 92 | 0.02 | DIV |
| blwp | 26 | 0.05 | BLWP context switch |


## Performance Targets

- **IPS Range**: 300,000 - 700,000
- **CPI Range**: 8 - 52
- **Primary Bottleneck**: memory, workspace

## Usage

```python
from tms9900_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

TI TMS9900 Users Guide
