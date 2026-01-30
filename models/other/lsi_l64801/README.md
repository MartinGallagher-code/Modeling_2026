# LSI Logic L64801

## Overview

**LSI Logic L64801** (1989) - First 3rd-party SPARC, gate-array

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1989 |
| Manufacturer | LSI Logic |
| Data Width | 32-bit |
| Clock | 25.0 MHz |
| Transistors | 200,000 |
| Technology | 0.8um gate array |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 18.0)
- **Typical CPI:** 1.8

## Performance

- **Estimated MIPS:** 13.9
- **Typical CPI:** 1.8

## Performance Model

### Usage

```python
from lsi_l64801_validated import LsiL64801Model

model = LsiL64801Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
lsi_l64801/
├── README.md                          # This documentation
├── current/
│   └── lsi_l64801_validated.py        # Validated model
├── validation/
│   └── lsi_l64801_validation.json     # Validation data
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
