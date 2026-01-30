# Cyrix Cx5x86

## Overview

**Cyrix Cx5x86** (1995) - Superscalar 486-socket chip, bridge to 6x86

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1995 |
| Manufacturer | Cyrix |
| Data Width | 32-bit |
| Clock | 100.0 MHz |
| Transistors | 2,000,000 |
| Technology | 0.65um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 18.0)
- **Typical CPI:** 1.5

## Performance

- **Estimated MIPS:** 66.7
- **Typical CPI:** 1.5

## Performance Model

### Usage

```python
from cx5x86_validated import Cx5x86Model

model = Cx5x86Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
cx5x86/
├── README.md                          # This documentation
├── current/
│   └── cx5x86_validated.py        # Validated model
├── validation/
│   └── cx5x86_validation.json     # Validation data
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
