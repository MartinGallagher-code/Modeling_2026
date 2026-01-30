# Zilog Z380

## Overview

**Zilog Z380** (1994) - 32-bit Z80 extension, Z80 compatibility

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1994 |
| Manufacturer | Zilog |
| Data Width | 32-bit |
| Clock | 20.0 MHz |
| Transistors | 200,000 |
| Technology | 0.6um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (2.0, 30.0)
- **Typical CPI:** 3.0

## Performance

- **Estimated MIPS:** 6.7
- **Typical CPI:** 3.0

## Performance Model

### Usage

```python
from z380_validated import Z380Model

model = Z380Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
z380/
├── README.md                          # This documentation
├── current/
│   └── z380_validated.py        # Validated model
├── validation/
│   └── z380_validation.json     # Validation data
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
