# Analog Devices ADSP-21020

## Overview

**Analog Devices ADSP-21020** (1990) - 32-bit floating-point SHARC predecessor

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1990 |
| Manufacturer | Analog Devices |
| Data Width | 32-bit |
| Clock | 33.0 MHz |
| Transistors | 450,000 |
| Technology | 0.8um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 2.0)
- **Typical CPI:** 1.2

## Performance

- **Estimated MIPS:** 27.5
- **Typical CPI:** 1.2

## Performance Model

### Usage

```python
from adsp21020_validated import Adsp21020Model

model = Adsp21020Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
adsp21020/
├── README.md                          # This documentation
├── current/
│   └── adsp21020_validated.py        # Validated model
├── validation/
│   └── adsp21020_validation.json     # Validation data
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
