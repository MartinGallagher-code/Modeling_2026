# Cyrix Cx486SLC

## Overview

**Cyrix Cx486SLC** (1992) - 486 ISA for 386SX systems, 16-bit bus

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1992 |
| Manufacturer | Cyrix |
| Data Width | 32-bit |
| Clock | 25.0 MHz |
| Transistors | 600,000 |
| Technology | 0.8um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.5, 30.0)
- **Typical CPI:** 3.0

## Performance

- **Estimated MIPS:** 8.3
- **Typical CPI:** 3.0

## Performance Model

### Usage

```python
from cx486slc_validated import Cx486slcModel

model = Cx486slcModel()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
cx486slc/
├── README.md                          # This documentation
├── current/
│   └── cx486slc_validated.py        # Validated model
├── validation/
│   └── cx486slc_validation.json     # Validation data
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
