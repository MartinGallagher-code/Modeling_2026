# Yamaha YM2610 OPNB

## Overview

**Yamaha YM2610 OPNB** (1988) - FM + ADPCM, Neo Geo audio standard

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1988 |
| Manufacturer | Yamaha |
| Data Width | 8-bit |
| Clock | 8.0 MHz |
| Transistors | 200,000 |
| Technology | 1.0um CMOS |

## Architecture

- **Data Width:** 8-bit
- **CPI Range:** (1.0, 3.0)
- **Typical CPI:** 2.3

## Performance

- **Estimated MIPS:** 3.5
- **Typical CPI:** 2.3

## Performance Model

### Usage

```python
from ym2610_validated import Ym2610Model

model = Ym2610Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
ym2610/
├── README.md                          # This documentation
├── current/
│   └── ym2610_validated.py        # Validated model
├── validation/
│   └── ym2610_validation.json     # Validation data
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
