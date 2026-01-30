# IBM RS64

## Overview

**IBM RS64** (1994) - POWER/PowerPC convergence, AS/400 transition

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1994 |
| Manufacturer | IBM |
| Data Width | 64-bit |
| Clock | 135.0 MHz |
| Transistors | 8,000,000 |
| Technology | 0.35um CMOS |

## Architecture

- **Data Width:** 64-bit
- **CPI Range:** (1.0, 10.0)
- **Typical CPI:** 0.7

## Performance

- **Estimated MIPS:** 192.9
- **Typical CPI:** 0.7

## Performance Model

### Usage

```python
from ibm_rs64_validated import IbmRs64Model

model = IbmRs64Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
ibm_rs64/
├── README.md                          # This documentation
├── current/
│   └── ibm_rs64_validated.py        # Validated model
├── validation/
│   └── ibm_rs64_validation.json     # Validation data
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
