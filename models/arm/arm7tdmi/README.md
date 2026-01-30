# ARM7TDMI

## Overview

**ARM7TDMI** (1994) - Thumb mode, hardware debug, dominant embedded core

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1994 |
| Manufacturer | ARM |
| Data Width | 32-bit |
| Clock | 40.0 MHz |
| Transistors | 74,000 |
| Technology | 0.6um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 12.0)
- **Typical CPI:** 1.5

## Performance

- **Estimated MIPS:** 26.7
- **Typical CPI:** 1.5

## Performance Model

### Usage

```python
from arm7tdmi_validated import Arm7tdmiModel

model = Arm7tdmiModel()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
arm7tdmi/
├── README.md                          # This documentation
├── current/
│   └── arm7tdmi_validated.py        # Validated model
├── validation/
│   └── arm7tdmi_validation.json     # Validation data
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
