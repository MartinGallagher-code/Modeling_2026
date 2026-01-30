# Soviet K1839VM1

## Overview

**Soviet K1839VM1** (1989) - VAX-compatible chip, Soviet 32-bit VAX clone

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1989 |
| Manufacturer | Angstrem |
| Data Width | 32-bit |
| Clock | 8.0 MHz |
| Transistors | 200,000 |
| Technology | 1.5um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (3.0, 45.0)
- **Typical CPI:** 4.0

## Performance

- **Estimated MIPS:** 2.0
- **Typical CPI:** 4.0

## Performance Model

### Usage

```python
from k1839vm1_validated import K1839vm1Model

model = K1839vm1Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
k1839vm1/
├── README.md                          # This documentation
├── current/
│   └── k1839vm1_validated.py        # Validated model
├── validation/
│   └── k1839vm1_validation.json     # Validation data
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
