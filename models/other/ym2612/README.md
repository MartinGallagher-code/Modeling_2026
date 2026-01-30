# Yamaha YM2612 OPN2

## Overview

**Yamaha YM2612 OPN2** (1988) - 6-channel FM synthesis, Sega Genesis audio

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1988 |
| Manufacturer | Yamaha |
| Data Width | 8-bit |
| Clock | 7.67 MHz |
| Transistors | 150,000 |
| Technology | 1.0um CMOS |

## Architecture

- **Data Width:** 8-bit
- **CPI Range:** (1.0, 3.0)
- **Typical CPI:** 2.5

## Performance

- **Estimated MIPS:** 3.1
- **Typical CPI:** 2.5

## Performance Model

### Usage

```python
from ym2612_validated import Ym2612Model

model = Ym2612Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
ym2612/
├── README.md                          # This documentation
├── current/
│   └── ym2612_validated.py        # Validated model
├── validation/
│   └── ym2612_validation.json     # Validation data
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
