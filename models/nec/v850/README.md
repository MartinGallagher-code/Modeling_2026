# NEC V850

## Overview

**NEC V850** (1994) - Embedded RISC for automotive ECUs

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1994 |
| Manufacturer | NEC |
| Data Width | 32-bit |
| Clock | 20.0 MHz |
| Transistors | 450,000 |
| Technology | 0.35um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 10.0)
- **Typical CPI:** 1.4

## Performance

- **Estimated MIPS:** 14.3
- **Typical CPI:** 1.4

## Performance Model

### Usage

```python
from v850_validated import V850Model

model = V850Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
v850/
├── README.md                          # This documentation
├── current/
│   └── v850_validated.py        # Validated model
├── validation/
│   └── v850_validation.json     # Validation data
├── measurements/                       # Calibration data
├── identification/                     # System ID results
└── docs/                              # Architecture docs
```

## Validation

| Test | Status |
|------|--------|
| CPI | ✓ Within 5% of target |
| Architecture | ✓ Cross-referenced with datasheets |

**Target Accuracy:** <5% CPI error

---

*Grey-Box Performance Modeling Research Project*
*Validated: January 2026*
