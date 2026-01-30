# IBM POWER2

## Overview

**IBM POWER2** (1993) - Enhanced POWER, 8-chip MCM, top TPC benchmarks

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1993 |
| Manufacturer | IBM |
| Data Width | 32-bit |
| Clock | 71.5 MHz |
| Transistors | 23,000,000 |
| Technology | 0.45um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 10.0)
- **Typical CPI:** 1.1

## Performance

- **Estimated MIPS:** 65.0
- **Typical CPI:** 1.1

## Performance Model

### Usage

```python
from ibm_power2_validated import IbmPower2Model

model = IbmPower2Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
ibm_power2/
├── README.md                          # This documentation
├── current/
│   └── ibm_power2_validated.py        # Validated model
├── validation/
│   └── ibm_power2_validation.json     # Validation data
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
