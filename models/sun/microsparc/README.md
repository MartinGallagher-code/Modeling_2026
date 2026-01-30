# Sun MicroSPARC

## Overview

**Sun MicroSPARC** (1992) - Low-cost single-chip SPARC, SPARCclassic/LX

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1992 |
| Manufacturer | Sun/Fujitsu |
| Data Width | 32-bit |
| Clock | 50.0 MHz |
| Transistors | 800,000 |
| Technology | 0.8um CMOS |

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
from microsparc_validated import MicrosparcModel

model = MicrosparcModel()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
microsparc/
├── README.md                          # This documentation
├── current/
│   └── microsparc_validated.py        # Validated model
├── validation/
│   └── microsparc_validation.json     # Validation data
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
