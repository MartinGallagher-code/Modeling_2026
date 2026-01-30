# HP PA-7200

## Overview

**HP PA-7200** (1994) - Superscalar PA-RISC, dual-issue

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1994 |
| Manufacturer | HP |
| Data Width | 32-bit |
| Clock | 140.0 MHz |
| Transistors | 1,260,000 |
| Technology | 0.5um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 10.0)
- **Typical CPI:** 0.9

## Performance

- **Estimated MIPS:** 155.6
- **Typical CPI:** 0.9

## Performance Model

### Usage

```python
from pa7200_validated import Pa7200Model

model = Pa7200Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
pa7200/
├── README.md                          # This documentation
├── current/
│   └── pa7200_validated.py        # Validated model
├── validation/
│   └── pa7200_validation.json     # Validation data
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
