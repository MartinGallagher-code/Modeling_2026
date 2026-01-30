# AMD Am486

## Overview

**AMD Am486** (1993) - AMD's 486 clone with write-back cache

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1993 |
| Manufacturer | AMD |
| Data Width | 32-bit |
| Clock | 40.0 MHz |
| Transistors | 1,200,000 |
| Technology | 0.7um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 25.0)
- **Typical CPI:** 1.8

## Performance

- **Estimated MIPS:** 22.2
- **Typical CPI:** 1.8

## Performance Model

### Usage

```python
from am486_validated import Am486Model

model = Am486Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
am486/
├── README.md                          # This documentation
├── current/
│   └── am486_validated.py        # Validated model
├── validation/
│   └── am486_validation.json     # Validation data
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
