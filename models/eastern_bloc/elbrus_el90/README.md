# Elbrus El-90

## Overview

**Elbrus El-90** (1990) - Soviet superscalar design, VLIW-like

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1990 |
| Manufacturer | MCST |
| Data Width | 64-bit |
| Clock | 50.0 MHz |
| Transistors | 2,000,000 |
| Technology | 0.8um CMOS |

## Architecture

- **Data Width:** 64-bit
- **CPI Range:** (1.0, 15.0)
- **Typical CPI:** 1.5

## Performance

- **Estimated MIPS:** 33.3
- **Typical CPI:** 1.5

## Performance Model

### Usage

```python
from elbrus_el90_validated import ElbrusEl90Model

model = ElbrusEl90Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
elbrus_el90/
├── README.md                          # This documentation
├── current/
│   └── elbrus_el90_validated.py        # Validated model
├── validation/
│   └── elbrus_el90_validation.json     # Validation data
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
