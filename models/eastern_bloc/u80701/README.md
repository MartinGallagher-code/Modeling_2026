# East German U80701

## Overview

**East German U80701** (1989) - DDR's last CPU project, 32-bit, cancelled with reunification

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1989 |
| Manufacturer | Kombinat Mikroelektronik |
| Data Width | 32-bit |
| Clock | 10.0 MHz |
| Transistors | 300,000 |
| Technology | 1.0um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (2.0, 35.0)
- **Typical CPI:** 3.5

## Performance

- **Estimated MIPS:** 2.9
- **Typical CPI:** 3.5

## Performance Model

### Usage

```python
from u80701_validated import U80701Model

model = U80701Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
u80701/
├── README.md                          # This documentation
├── current/
│   └── u80701_validated.py        # Validated model
├── validation/
│   └── u80701_validation.json     # Validation data
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
