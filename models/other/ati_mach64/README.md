# ATI Mach64

## Overview

**ATI Mach64** (1994) - Hardware video playback, foundation for Rage line

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1994 |
| Manufacturer | ATI |
| Data Width | 32-bit |
| Clock | 66.0 MHz |
| Transistors | 1,000,000 |
| Technology | 0.5um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 3.0)
- **Typical CPI:** 1.5

## Performance

- **Estimated MIPS:** 44.0
- **Typical CPI:** 1.5

## Performance Model

### Usage

```python
from ati_mach64_validated import AtiMach64Model

model = AtiMach64Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
ati_mach64/
├── README.md                          # This documentation
├── current/
│   └── ati_mach64_validated.py        # Validated model
├── validation/
│   └── ati_mach64_validation.json     # Validation data
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
