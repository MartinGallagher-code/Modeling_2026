# S3 86C911

## Overview

**S3 86C911** (1991) - First mass-market 2D accelerator

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1991 |
| Manufacturer | S3 |
| Data Width | 32-bit |
| Clock | 40.0 MHz |
| Transistors | 350,000 |
| Technology | 0.8um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 3.0)
- **Typical CPI:** 2.0

## Performance

- **Estimated MIPS:** 20.0
- **Typical CPI:** 2.0

## Performance Model

### Usage

```python
from s3_86c911_validated import S386c911Model

model = S386c911Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
s3_86c911/
├── README.md                          # This documentation
├── current/
│   └── s3_86c911_validated.py        # Validated model
├── validation/
│   └── s3_86c911_validation.json     # Validation data
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
