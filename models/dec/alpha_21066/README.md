# DEC Alpha 21066

## Overview

**DEC Alpha 21066** (1993) - Low-cost Alpha with integrated PCI/memory controller

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1993 |
| Manufacturer | DEC |
| Data Width | 64-bit |
| Clock | 166.0 MHz |
| Transistors | 1,750,000 |
| Technology | 0.675um CMOS |

## Architecture

- **Data Width:** 64-bit
- **CPI Range:** (1.0, 15.0)
- **Typical CPI:** 1.3

## Performance

- **Estimated MIPS:** 127.7
- **Typical CPI:** 1.3

## Performance Model

### Usage

```python
from alpha_21066_validated import Alpha21066Model

model = Alpha21066Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
alpha_21066/
├── README.md                          # This documentation
├── current/
│   └── alpha_21066_validated.py        # Validated model
├── validation/
│   └── alpha_21066_validation.json     # Validation data
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
