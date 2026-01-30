# IBM 486SLC2

## Overview

**IBM 486SLC2** (1992) - IBM's 486-class chip, used in ThinkPads

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1992 |
| Manufacturer | IBM |
| Data Width | 32-bit |
| Clock | 50.0 MHz |
| Transistors | 1,400,000 |
| Technology | 0.8um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 25.0)
- **Typical CPI:** 2.2

## Performance

- **Estimated MIPS:** 22.7
- **Typical CPI:** 2.2

## Performance Model

### Usage

```python
from ibm_486slc2_validated import Ibm486slc2Model

model = Ibm486slc2Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
ibm_486slc2/
├── README.md                          # This documentation
├── current/
│   └── ibm_486slc2_validated.py        # Validated model
├── validation/
│   └── ibm_486slc2_validation.json     # Validation data
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
