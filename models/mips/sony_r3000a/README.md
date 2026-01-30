# Sony CXD8530BQ

## Overview

**Sony CXD8530BQ** (1994) - PlayStation CPU, MIPS R3000A with GTE coprocessor

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1994 |
| Manufacturer | Sony/LSI Logic |
| Data Width | 32-bit |
| Clock | 33.8688 MHz |
| Transistors | 300,000 |
| Technology | 0.6um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 12.0)
- **Typical CPI:** 1.4

## Performance

- **Estimated MIPS:** 24.2
- **Typical CPI:** 1.4

## Performance Model

### Usage

```python
from sony_r3000a_validated import SonyR3000aModel

model = SonyR3000aModel()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
sony_r3000a/
├── README.md                          # This documentation
├── current/
│   └── sony_r3000a_validated.py        # Validated model
├── validation/
│   └── sony_r3000a_validation.json     # Validation data
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
