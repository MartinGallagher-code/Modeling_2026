# Fujitsu SPARClite

## Overview

**Fujitsu SPARClite** (1993) - Embedded SPARC variant, no FPU, low power

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1993 |
| Manufacturer | Fujitsu |
| Data Width | 32-bit |
| Clock | 50.0 MHz |
| Transistors | 500,000 |
| Technology | 0.5um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 18.0)
- **Typical CPI:** 1.6

## Performance

- **Estimated MIPS:** 31.2
- **Typical CPI:** 1.6

## Performance Model

### Usage

```python
from sparclite_validated import SparcliteModel

model = SparcliteModel()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
sparclite/
├── README.md                          # This documentation
├── current/
│   └── sparclite_validated.py        # Validated model
├── validation/
│   └── sparclite_validation.json     # Validation data
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
