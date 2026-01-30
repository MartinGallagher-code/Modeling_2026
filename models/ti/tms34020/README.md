# TI TMS34020

## Overview

**TI TMS34020** (1988) - Enhanced 34010 GPU, hardware pixel processing

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1988 |
| Manufacturer | TI |
| Data Width | 32-bit |
| Clock | 40.0 MHz |
| Transistors | 500,000 |
| Technology | 0.8um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 3.0)
- **Typical CPI:** 2.0

## Performance

- **Estimated MIPS:** 20.0
- **Typical CPI:** 2.0

## Performance Model

### Usage

```python
from tms34020_validated import Tms34020Model

model = Tms34020Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
tms34020/
├── README.md                          # This documentation
├── current/
│   └── tms34020_validated.py        # Validated model
├── validation/
│   └── tms34020_validation.json     # Validation data
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
