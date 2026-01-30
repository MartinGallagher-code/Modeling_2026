# Yamaha YMF262 OPL3

## Overview

**Yamaha YMF262 OPL3** (1990) - 4-operator FM, Sound Blaster 16 standard

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1990 |
| Manufacturer | Yamaha |
| Data Width | 8-bit |
| Clock | 14.32 MHz |
| Transistors | 180,000 |
| Technology | 0.8um CMOS |

## Architecture

- **Data Width:** 8-bit
- **CPI Range:** (1.0, 2.0)
- **Typical CPI:** 2.0

## Performance

- **Estimated MIPS:** 7.2
- **Typical CPI:** 2.0

## Performance Model

### Usage

```python
from ymf262_validated import Ymf262Model

model = Ymf262Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
ymf262/
├── README.md                          # This documentation
├── current/
│   └── ymf262_validated.py        # Validated model
├── validation/
│   └── ymf262_validation.json     # Validation data
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
