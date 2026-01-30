# SGS-Thomson D950

## Overview

**SGS-Thomson D950** (1991) - European DSP for GSM baseband processing

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1991 |
| Manufacturer | SGS-Thomson |
| Data Width | 16-bit |
| Clock | 20.0 MHz |
| Transistors | 250,000 |
| Technology | 0.8um CMOS |

## Architecture

- **Data Width:** 16-bit
- **CPI Range:** (1.0, 3.0)
- **Typical CPI:** 1.4

## Performance

- **Estimated MIPS:** 14.3
- **Typical CPI:** 1.4

## Performance Model

### Usage

```python
from sgs_d950_validated import SgsD950Model

model = SgsD950Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
sgs_d950/
├── README.md                          # This documentation
├── current/
│   └── sgs_d950_validated.py        # Validated model
├── validation/
│   └── sgs_d950_validation.json     # Validation data
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
