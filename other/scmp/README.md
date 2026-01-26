# National SC/MP Performance Model

Grey-box queueing model for the National SC/MP microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1974 |
| Clock | 1.0 MHz |
| Bus Width | 8-bit |
| Transistors | 5,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| implied | 7 | 0.20 | Implied |
| immediate | 10 | 0.18 | Immediate |
| memory | 18 | 0.20 | Memory |
| auto_indexed | 18 | 0.10 | Auto-indexed |
| branch | 9 | 0.12 | Branch |
| transfer | 7 | 0.10 | Transfer |
| io | 22 | 0.05 | I/O |
| misc | 7 | 0.05 | Other |


## Performance Targets

- **IPS Range**: 50,000 - 150,000
- **CPI Range**: 7 - 22
- **Primary Bottleneck**: fetch, serial_bus

## Usage

```python
from scmp_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

National SC/MP Programmers Guide
