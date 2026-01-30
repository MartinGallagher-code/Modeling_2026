# AMD Am5x86

## Overview

**AMD Am5x86** (1995) - 486 with 4x clock, Pentium-class performance

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1995 |
| Manufacturer | AMD |
| Data Width | 32-bit |
| Clock | 133.0 MHz |
| Transistors | 1,600,000 |
| Technology | 0.35um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 22.0)
- **Typical CPI:** 1.6

## Performance

- **Estimated MIPS:** 83.1
- **Typical CPI:** 1.6

## Performance Model

### Usage

```python
from am5x86_validated import Am5x86Model

model = Am5x86Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
am5x86/
├── README.md                          # This documentation
├── current/
│   └── am5x86_validated.py        # Validated model
├── validation/
│   └── am5x86_validation.json     # Validation data
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
