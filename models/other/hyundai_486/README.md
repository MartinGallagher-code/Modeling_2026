# Hyundai 80486 Clone

## Overview

**Hyundai 80486 Clone** (1993) - Korean 486-compatible, beginning of Korean CPU efforts

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1993 |
| Manufacturer | Hyundai |
| Data Width | 32-bit |
| Clock | 33.0 MHz |
| Transistors | 1,200,000 |
| Technology | 0.7um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 25.0)
- **Typical CPI:** 1.9

## Performance

- **Estimated MIPS:** 17.4
- **Typical CPI:** 1.9

## Performance Model

### Usage

```python
from hyundai_486_validated import Hyundai486Model

model = Hyundai486Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
hyundai_486/
├── README.md                          # This documentation
├── current/
│   └── hyundai_486_validated.py        # Validated model
├── validation/
│   └── hyundai_486_validation.json     # Validation data
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
