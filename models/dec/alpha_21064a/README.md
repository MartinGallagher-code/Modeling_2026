# DEC Alpha 21064A

## Overview

**DEC Alpha 21064A** (1994) - Faster 21064, 300 MHz

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1994 |
| Manufacturer | DEC |
| Data Width | 64-bit |
| Clock | 300.0 MHz |
| Transistors | 2,850,000 |
| Technology | 0.5um CMOS |

## Architecture

- **Data Width:** 64-bit
- **CPI Range:** (1.0, 12.0)
- **Typical CPI:** 1.2

## Performance

- **Estimated MIPS:** 250.0
- **Typical CPI:** 1.2

## Performance Model

### Usage

```python
from alpha_21064a_validated import Alpha21064aModel

model = Alpha21064aModel()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
alpha_21064a/
├── README.md                          # This documentation
├── current/
│   └── alpha_21064a_validated.py        # Validated model
├── validation/
│   └── alpha_21064a_validation.json     # Validation data
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
