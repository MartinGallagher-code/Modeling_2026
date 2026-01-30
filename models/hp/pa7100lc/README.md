# HP PA-7100LC

## Overview

**HP PA-7100LC** (1994) - Low-cost PA-RISC with on-chip cache/memory controller

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1994 |
| Manufacturer | HP |
| Data Width | 32-bit |
| Clock | 100.0 MHz |
| Transistors | 900,000 |
| Technology | 0.5um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 14.0)
- **Typical CPI:** 1.4

## Performance

- **Estimated MIPS:** 71.4
- **Typical CPI:** 1.4

## Performance Model

### Usage

```python
from pa7100lc_validated import Pa7100lcModel

model = Pa7100lcModel()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
pa7100lc/
├── README.md                          # This documentation
├── current/
│   └── pa7100lc_validated.py        # Validated model
├── validation/
│   └── pa7100lc_validation.json     # Validation data
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
