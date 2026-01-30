# PowerPC 604

## Overview

**PowerPC 604** (1994) - High-performance PowerPC, 4-issue superscalar

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1994 |
| Manufacturer | Motorola/IBM |
| Data Width | 32-bit |
| Clock | 133.0 MHz |
| Transistors | 3,600,000 |
| Technology | 0.5um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 13.0)
- **Typical CPI:** 0.8

## Performance

- **Estimated MIPS:** 166.2
- **Typical CPI:** 0.8

## Performance Model

### Usage

```python
from ppc604_validated import Ppc604Model

model = Ppc604Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
ppc604/
├── README.md                          # This documentation
├── current/
│   └── ppc604_validated.py        # Validated model
├── validation/
│   └── ppc604_validation.json     # Validation data
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
