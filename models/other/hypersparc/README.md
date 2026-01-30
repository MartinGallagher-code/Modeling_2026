# Ross HyperSPARC

## Overview

**Ross HyperSPARC** (1993) - 3rd-party SPARC, SPARCstation 20

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1993 |
| Manufacturer | Ross/Cypress |
| Data Width | 32-bit |
| Clock | 150.0 MHz |
| Transistors | 1,800,000 |
| Technology | 0.5um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 12.0)
- **Typical CPI:** 1.1

## Performance

- **Estimated MIPS:** 136.4
- **Typical CPI:** 1.1

## Performance Model

### Usage

```python
from hypersparc_validated import HypersparcModel

model = HypersparcModel()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
hypersparc/
├── README.md                          # This documentation
├── current/
│   └── hypersparc_validated.py        # Validated model
├── validation/
│   └── hypersparc_validation.json     # Validation data
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
