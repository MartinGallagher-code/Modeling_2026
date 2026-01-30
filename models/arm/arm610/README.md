# ARM610

## Overview

**ARM610** (1993) - First ARM6 variant, Acorn RiscPC, Apple Newton

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1993 |
| Manufacturer | ARM/VLSI |
| Data Width | 32-bit |
| Clock | 33.0 MHz |
| Transistors | 84,000 |
| Technology | 0.6um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 16.0)
- **Typical CPI:** 1.5

## Performance

- **Estimated MIPS:** 22.0
- **Typical CPI:** 1.5

## Performance Model

### Usage

```python
from arm610_validated import Arm610Model

model = Arm610Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
arm610/
├── README.md                          # This documentation
├── current/
│   └── arm610_validated.py        # Validated model
├── validation/
│   └── arm610_validation.json     # Validation data
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
