# Inmos T414 Performance Model

Grey-box queueing model for the Inmos T414 microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | 1985 |
| Clock | 15.0 MHz |
| Bus Width | 32-bit |
| Transistors | 200,000 |

## Timing Categories

| Category | Cycles | Weight | Description |
|----------|--------|--------|-------------|
| direct | 1 | 0.35 | Direct functions |
| indirect | 2 | 0.20 | Indirect functions |
| load_store | 2 | 0.15 | Load/Store |
| jump | 3 | 0.10 | Jump |
| call | 4 | 0.05 | CALL |
| channel | 6 | 0.08 | Channel comms |
| alt | 10 | 0.03 | ALT |
| misc | 1 | 0.04 | Other |


## Performance Targets

- **IPS Range**: 5,000,000 - 10,000,000
- **CPI Range**: 1 - 6
- **Primary Bottleneck**: memory, channel

## Usage

```python
from t414_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

Inmos T414 Technical Manual
