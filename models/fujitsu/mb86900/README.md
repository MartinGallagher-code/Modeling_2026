# Fujitsu MB86900

## Overview

**Fujitsu MB86900** (1986) - First silicon SPARC implementation, Sun-4 workstations

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1986 |
| Manufacturer | Fujitsu |
| Data Width | 32-bit |
| Clock | 16.7 MHz |
| Transistors | 75,000 |
| Technology | 1.5um gate array |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 20.0)
- **Typical CPI:** 1.8

## Performance

- **Estimated MIPS:** 9.3
- **Typical CPI:** 1.8

## Performance Model

### Usage

```python
from mb86900_validated import Mb86900Model

model = Mb86900Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
mb86900/
├── README.md                          # This documentation
├── current/
│   └── mb86900_validated.py        # Validated model
├── validation/
│   └── mb86900_validation.json     # Validation data
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
