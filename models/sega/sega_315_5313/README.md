# Sega 315-5313 VDP

## Overview

**Sega 315-5313 VDP** (1988) - Genesis/Mega Drive video, dual playfields

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1988 |
| Manufacturer | Sega/Yamaha |
| Data Width | 16-bit |
| Clock | 13.42 MHz |
| Transistors | 120,000 |
| Technology | 0.8um CMOS |

## Architecture

- **Data Width:** 16-bit
- **CPI Range:** (1.0, 4.0)
- **Typical CPI:** 3.0

## Performance

- **Estimated MIPS:** 4.5
- **Typical CPI:** 3.0

## Performance Model

### Usage

```python
from sega_315_5313_validated import Sega3155313Model

model = Sega3155313Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
sega_315_5313/
├── README.md                          # This documentation
├── current/
│   └── sega_315_5313_validated.py        # Validated model
├── validation/
│   └── sega_315_5313_validation.json     # Validation data
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
