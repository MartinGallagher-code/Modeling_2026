# Sun UltraSPARC I

## Overview

**Sun UltraSPARC I** (1995) - 64-bit SPARC V9, VIS multimedia instructions

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1995 |
| Manufacturer | Sun/TI |
| Data Width | 64-bit |
| Clock | 167.0 MHz |
| Transistors | 5,200,000 |
| Technology | 0.47um CMOS |

## Architecture

- **Data Width:** 64-bit
- **CPI Range:** (1.0, 10.0)
- **Typical CPI:** 0.7

## Performance

- **Estimated MIPS:** 238.6
- **Typical CPI:** 0.7

## Performance Model

### Usage

```python
from ultrasparc_i_validated import UltrasparcIModel

model = UltrasparcIModel()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
ultrasparc_i/
├── README.md                          # This documentation
├── current/
│   └── ultrasparc_i_validated.py        # Validated model
├── validation/
│   └── ultrasparc_i_validation.json     # Validation data
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
