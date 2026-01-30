# Sun SuperSPARC

## Overview

**Sun SuperSPARC** (1992) - 3-issue superscalar SPARC, SPARCstation 10/20

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1992 |
| Manufacturer | TI/Sun |
| Data Width | 32-bit |
| Clock | 50.0 MHz |
| Transistors | 3,100,000 |
| Technology | 0.8um BiCMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 12.0)
- **Typical CPI:** 0.8

## Performance

- **Estimated MIPS:** 62.5
- **Typical CPI:** 0.8

## Performance Model

### Usage

```python
from supersparc_validated import SupersparcModel

model = SupersparcModel()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
supersparc/
├── README.md                          # This documentation
├── current/
│   └── supersparc_validated.py        # Validated model
├── validation/
│   └── supersparc_validation.json     # Validation data
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
