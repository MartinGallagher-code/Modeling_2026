# SGI R10000

## Overview

**SGI R10000** (1994) - Out-of-order MIPS, register renaming

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1994 |
| Manufacturer | MIPS/SGI |
| Data Width | 64-bit |
| Clock | 200.0 MHz |
| Transistors | 6,800,000 |
| Technology | 0.35um CMOS |

## Architecture

- **Data Width:** 64-bit
- **CPI Range:** (1.0, 8.0)
- **Typical CPI:** 0.6

## Performance

- **Estimated MIPS:** 333.3
- **Typical CPI:** 0.6

## Performance Model

### Usage

```python
from mips_r10000_validated import MipsR10000Model

model = MipsR10000Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
mips_r10000/
├── README.md                          # This documentation
├── current/
│   └── mips_r10000_validated.py        # Validated model
├── validation/
│   └── mips_r10000_validation.json     # Validation data
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
