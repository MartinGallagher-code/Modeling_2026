# SPARC64 (Hal)

## Overview

**SPARC64 (Hal)** (1995) - 64-bit SPARC V9 from Fujitsu/Hal Computer

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1995 |
| Manufacturer | Hal/Fujitsu |
| Data Width | 64-bit |
| Clock | 101.0 MHz |
| Transistors | 3,500,000 |
| Technology | 0.4um CMOS |

## Architecture

- **Data Width:** 64-bit
- **CPI Range:** (1.0, 12.0)
- **Typical CPI:** 0.8

## Performance

- **Estimated MIPS:** 126.2
- **Typical CPI:** 0.8

## Performance Model

### Usage

```python
from sparc64_hal_validated import Sparc64HalModel

model = Sparc64HalModel()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
sparc64_hal/
├── README.md                          # This documentation
├── current/
│   └── sparc64_hal_validated.py        # Validated model
├── validation/
│   └── sparc64_hal_validation.json     # Validation data
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
