# Hitachi SH-2

## Overview

**Hitachi SH-2** (1994) - Dual SH-2 in Sega Saturn, 5-stage pipeline

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1994 |
| Manufacturer | Hitachi |
| Data Width | 32-bit |
| Clock | 28.6 MHz |
| Transistors | 700,000 |
| Technology | 0.5um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 8.0)
- **Typical CPI:** 1.3

## Performance

- **Estimated MIPS:** 22.0
- **Typical CPI:** 1.3

## Performance Model

### Usage

```python
from sh2_validated import Sh2Model

model = Sh2Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
sh2/
├── README.md                          # This documentation
├── current/
│   └── sh2_validated.py        # Validated model
├── validation/
│   └── sh2_validation.json     # Validation data
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
