# C&T 65545

## Overview

**C&T 65545** (1993) - Laptop graphics with power management

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1993 |
| Manufacturer | Chips & Technologies |
| Data Width | 32-bit |
| Clock | 40.0 MHz |
| Transistors | 500,000 |
| Technology | 0.5um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 3.0)
- **Typical CPI:** 2.5

## Performance

- **Estimated MIPS:** 16.0
- **Typical CPI:** 2.5

## Performance Model

### Usage

```python
from ct65545_validated import Ct65545Model

model = Ct65545Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
ct65545/
├── README.md                          # This documentation
├── current/
│   └── ct65545_validated.py        # Validated model
├── validation/
│   └── ct65545_validation.json     # Validation data
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
