# ATI Mach32

## Overview

**ATI Mach32** (1992) - ATI's first true graphics coprocessor

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1992 |
| Manufacturer | ATI |
| Data Width | 32-bit |
| Clock | 44.0 MHz |
| Transistors | 600,000 |
| Technology | 0.6um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 3.0)
- **Typical CPI:** 1.8

## Performance

- **Estimated MIPS:** 24.4
- **Typical CPI:** 1.8

## Performance Model

### Usage

```python
from ati_mach32_validated import AtiMach32Model

model = AtiMach32Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
ati_mach32/
├── README.md                          # This documentation
├── current/
│   └── ati_mach32_validated.py        # Validated model
├── validation/
│   └── ati_mach32_validation.json     # Validation data
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
