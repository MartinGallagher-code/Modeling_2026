# Hudson HuC6280

## Overview

**Hudson HuC6280** (1987) - TurboGrafx-16 CPU, enhanced 65C02 with speed modes

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1987 |
| Manufacturer | Hudson Soft |
| Data Width | 8-bit |
| Clock | 7.16 MHz |
| Transistors | 40,000 |
| Technology | 0.8um CMOS |

## Architecture

- **Data Width:** 8-bit
- **CPI Range:** (2.0, 18.0)
- **Typical CPI:** 3.5

## Performance

- **Estimated MIPS:** 2.0
- **Typical CPI:** 3.5

## Performance Model

### Usage

```python
from huc6280_validated import Huc6280Model

model = Huc6280Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
huc6280/
├── README.md                          # This documentation
├── current/
│   └── huc6280_validated.py        # Validated model
├── validation/
│   └── huc6280_validation.json     # Validation data
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
