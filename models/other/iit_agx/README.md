# IIT AGX

## Overview

**IIT AGX** (1993) - XGA-compatible graphics accelerator

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1993 |
| Manufacturer | IIT |
| Data Width | 32-bit |
| Clock | 50.0 MHz |
| Transistors | 400,000 |
| Technology | 0.6um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 3.0)
- **Typical CPI:** 2.2

## Performance

- **Estimated MIPS:** 22.7
- **Typical CPI:** 2.2

## Performance Model

### Usage

```python
from iit_agx_validated import IitAgxModel

model = IitAgxModel()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
iit_agx/
├── README.md                          # This documentation
├── current/
│   └── iit_agx_validated.py        # Validated model
├── validation/
│   └── iit_agx_validation.json     # Validation data
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
