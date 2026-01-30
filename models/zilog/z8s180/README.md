# Zilog Z8S180

## Overview

**Zilog Z8S180** (1988) - Enhanced Z180 with DMA and serial

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1988 |
| Manufacturer | Zilog |
| Data Width | 8-bit |
| Clock | 20.0 MHz |
| Transistors | 80,000 |
| Technology | 0.8um CMOS |

## Architecture

- **Data Width:** 8-bit
- **CPI Range:** (2.0, 20.0)
- **Typical CPI:** 3.5

## Performance

- **Estimated MIPS:** 5.7
- **Typical CPI:** 3.5

## Performance Model

### Usage

```python
from z8s180_validated import Z8s180Model

model = Z8s180Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
z8s180/
├── README.md                          # This documentation
├── current/
│   └── z8s180_validated.py        # Validated model
├── validation/
│   └── z8s180_validation.json     # Validation data
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
