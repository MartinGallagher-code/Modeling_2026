# Toshiba TX39

## Overview

**Toshiba TX39** (1994) - MIPS R3900-based embedded core for PDAs

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1994 |
| Manufacturer | Toshiba |
| Data Width | 32-bit |
| Clock | 66.0 MHz |
| Transistors | 700,000 |
| Technology | 0.35um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 12.0)
- **Typical CPI:** 1.4

## Performance

- **Estimated MIPS:** 47.1
- **Typical CPI:** 1.4

## Performance Model

### Usage

```python
from tx39_validated import Tx39Model

model = Tx39Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
tx39/
├── README.md                          # This documentation
├── current/
│   └── tx39_validated.py        # Validated model
├── validation/
│   └── tx39_validation.json     # Validation data
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
