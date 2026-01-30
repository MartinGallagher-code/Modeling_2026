# IBM POWER1

## Overview

**IBM POWER1** (1990) - Original POWER architecture, RS/6000, foundation of PowerPC

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1990 |
| Manufacturer | IBM |
| Data Width | 32-bit |
| Clock | 25.0 MHz |
| Transistors | 6,900,000 |
| Technology | 1.0um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 13.0)
- **Typical CPI:** 1.4

## Performance

- **Estimated MIPS:** 17.9
- **Typical CPI:** 1.4

## Performance Model

### Usage

```python
from ibm_power1_validated import IbmPower1Model

model = IbmPower1Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
ibm_power1/
├── README.md                          # This documentation
├── current/
│   └── ibm_power1_validated.py        # Validated model
├── validation/
│   └── ibm_power1_validation.json     # Validation data
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
