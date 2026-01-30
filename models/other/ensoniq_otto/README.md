# Ensoniq OTTO (ES5505)

## Overview

**Ensoniq OTTO (ES5505)** (1991) - 32-voice wavetable, Gravis Ultrasound / Taito F3

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1991 |
| Manufacturer | Ensoniq |
| Data Width | 16-bit |
| Clock | 16.0 MHz |
| Transistors | 250,000 |
| Technology | 0.8um CMOS |

## Architecture

- **Data Width:** 16-bit
- **CPI Range:** (1.0, 3.0)
- **Typical CPI:** 2.2

## Performance

- **Estimated MIPS:** 7.3
- **Typical CPI:** 2.2

## Performance Model

### Usage

```python
from ensoniq_otto_validated import EnsoniqOttoModel

model = EnsoniqOttoModel()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
ensoniq_otto/
├── README.md                          # This documentation
├── current/
│   └── ensoniq_otto_validated.py        # Validated model
├── validation/
│   └── ensoniq_otto_validation.json     # Validation data
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
