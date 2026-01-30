# MIPS R4400

## Overview

**MIPS R4400** (1993) - Improved R4000 with larger caches, SGI Indy/Indigo2

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1993 |
| Manufacturer | MIPS |
| Data Width | 64-bit |
| Clock | 250.0 MHz |
| Transistors | 2,300,000 |
| Technology | 0.6um CMOS |

## Architecture

- **Data Width:** 64-bit
- **CPI Range:** (1.0, 14.0)
- **Typical CPI:** 1.4

## Performance

- **Estimated MIPS:** 178.6
- **Typical CPI:** 1.4

## Performance Model

### Usage

```python
from mips_r4400_validated import MipsR4400Model

model = MipsR4400Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
mips_r4400/
├── README.md                          # This documentation
├── current/
│   └── mips_r4400_validated.py        # Validated model
├── validation/
│   └── mips_r4400_validation.json     # Validation data
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
