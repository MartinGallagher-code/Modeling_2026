# ARM250

## Overview

**ARM250** (1990) - ARM2 with MMU, MEMC, VIDC integrated, Acorn A3000

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1990 |
| Manufacturer | ARM/VLSI |
| Data Width | 32-bit |
| Clock | 12.0 MHz |
| Transistors | 100,000 |
| Technology | 1.0um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 30.0)
- **Typical CPI:** 1.7

## Performance

- **Estimated MIPS:** 7.1
- **Typical CPI:** 1.7

## Performance Model

### Usage

```python
from arm250_validated import Arm250Model

model = Arm250Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
arm250/
├── README.md                          # This documentation
├── current/
│   └── arm250_validated.py        # Validated model
├── validation/
│   └── arm250_validation.json     # Validation data
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
