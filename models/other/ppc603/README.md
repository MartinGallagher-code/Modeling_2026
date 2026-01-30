# PowerPC 603

## Overview

**PowerPC 603** (1993) - Low-power PowerPC, 5-stage pipeline, PowerBook 5300

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1993 |
| Manufacturer | Motorola/IBM |
| Data Width | 32-bit |
| Clock | 80.0 MHz |
| Transistors | 1,600,000 |
| Technology | 0.5um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 19.0)
- **Typical CPI:** 1.3

## Performance

- **Estimated MIPS:** 61.5
- **Typical CPI:** 1.3

## Performance Model

### Usage

```python
from ppc603_validated import Ppc603Model

model = Ppc603Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
ppc603/
├── README.md                          # This documentation
├── current/
│   └── ppc603_validated.py        # Validated model
├── validation/
│   └── ppc603_validation.json     # Validation data
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
