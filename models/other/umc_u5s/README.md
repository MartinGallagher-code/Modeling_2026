# UMC U5S Green CPU

## Overview

**UMC U5S Green CPU** (1994) - Taiwanese 486 clone, super low power

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1994 |
| Manufacturer | UMC |
| Data Width | 32-bit |
| Clock | 40.0 MHz |
| Transistors | 1,200,000 |
| Technology | 0.5um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 25.0)
- **Typical CPI:** 1.9

## Performance

- **Estimated MIPS:** 21.1
- **Typical CPI:** 1.9

## Performance Model

### Usage

```python
from umc_u5s_validated import UmcU5sModel

model = UmcU5sModel()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
umc_u5s/
├── README.md                          # This documentation
├── current/
│   └── umc_u5s_validated.py        # Validated model
├── validation/
│   └── umc_u5s_validation.json     # Validation data
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
