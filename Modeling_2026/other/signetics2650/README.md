# Signetics 2650 Performance Model

Grey-box queueing model for the Signetics 2650 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1975 |
| Clock | 1.25 MHz |
| Bus Width | 8-bit |
| Transistors | 6,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| register | 2 | 0.25 | Register ops |
| immediate | 4 | 0.18 | Immediate |
| absolute | 6 | 0.15 | Absolute |
| relative | 6 | 0.12 | Relative |
| indirect | 9 | 0.08 | Indirect |
| branch | 5 | 0.10 | Branch |
| call_return | 9 | 0.07 | ZBSR, RETC |
| io | 6 | 0.05 | I/O |


## Performance Targets

- **IPS Range**: 200,000 - 500,000
- **CPI Range**: 2 - 9
- **Primary Bottleneck**: fetch, decode

## Usage

```python
from signetics2650_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

Signetics 2650 Microprocessor Manual
