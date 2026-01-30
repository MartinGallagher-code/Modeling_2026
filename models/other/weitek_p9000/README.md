# Weitek P9000

## Overview

**Weitek P9000** (1991) - High-end 2D coprocessor, Diamond Viper/NeXT

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1991 |
| Manufacturer | Weitek |
| Data Width | 32-bit |
| Clock | 40.0 MHz |
| Transistors | 500,000 |
| Technology | 0.8um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 3.0)
- **Typical CPI:** 1.8

## Performance

- **Estimated MIPS:** 22.2
- **Typical CPI:** 1.8

## Performance Model

### Usage

```python
from weitek_p9000_validated import WeitekP9000Model

model = WeitekP9000Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
weitek_p9000/
├── README.md                          # This documentation
├── current/
│   └── weitek_p9000_validated.py        # Validated model
├── validation/
│   └── weitek_p9000_validation.json     # Validation data
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
