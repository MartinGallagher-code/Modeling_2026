# Sun MicroSPARC II

## Overview

**Sun MicroSPARC II** (1994) - Enhanced MicroSPARC, SPARCstation 5

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1994 |
| Manufacturer | Sun |
| Data Width | 32-bit |
| Clock | 110.0 MHz |
| Transistors | 2,300,000 |
| Technology | 0.5um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 14.0)
- **Typical CPI:** 1.3

## Performance

- **Estimated MIPS:** 84.6
- **Typical CPI:** 1.3

## Performance Model

### Usage

```python
from microsparc_ii_validated import MicrosparcIiModel

model = MicrosparcIiModel()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
microsparc_ii/
├── README.md                          # This documentation
├── current/
│   └── microsparc_ii_validated.py        # Validated model
├── validation/
│   └── microsparc_ii_validation.json     # Validation data
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
