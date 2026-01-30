# Samsung KS86C4004

## Overview

**Samsung KS86C4004** (1990) - Samsung's 4-bit/8-bit MCU, early Korean semiconductor

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1990 |
| Manufacturer | Samsung |
| Data Width | 8-bit |
| Clock | 10.0 MHz |
| Transistors | 50,000 |
| Technology | 1.0um CMOS |

## Architecture

- **Data Width:** 8-bit
- **CPI Range:** (2.0, 20.0)
- **Typical CPI:** 3.0

## Performance

- **Estimated MIPS:** 3.3
- **Typical CPI:** 3.0

## Performance Model

### Usage

```python
from ks86c4004_validated import Ks86c4004Model

model = Ks86c4004Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
ks86c4004/
├── README.md                          # This documentation
├── current/
│   └── ks86c4004_validated.py        # Validated model
├── validation/
│   └── ks86c4004_validation.json     # Validation data
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
