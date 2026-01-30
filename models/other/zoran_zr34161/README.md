# Zoran ZR34161

## Overview

**Zoran ZR34161** (1991) - JPEG/MPEG decoder DSP, early digital imaging

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1991 |
| Manufacturer | Zoran |
| Data Width | 16-bit |
| Clock | 25.0 MHz |
| Transistors | 300,000 |
| Technology | 0.8um CMOS |

## Architecture

- **Data Width:** 16-bit
- **CPI Range:** (1.0, 2.0)
- **Typical CPI:** 1.5

## Performance

- **Estimated MIPS:** 16.7
- **Typical CPI:** 1.5

## Performance Model

### Usage

```python
from zoran_zr34161_validated import ZoranZr34161Model

model = ZoranZr34161Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
zoran_zr34161/
├── README.md                          # This documentation
├── current/
│   └── zoran_zr34161_validated.py        # Validated model
├── validation/
│   └── zoran_zr34161_validation.json     # Validation data
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
