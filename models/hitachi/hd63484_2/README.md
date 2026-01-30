# Hitachi HD63484-2 ACRTC

## Overview

**Hitachi HD63484-2 ACRTC** (1987) - Enhanced ACRTC, faster drawing commands

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1987 |
| Manufacturer | Hitachi |
| Data Width | 16-bit |
| Clock | 10.0 MHz |
| Transistors | 120,000 |
| Technology | 1.0um CMOS |

## Architecture

- **Data Width:** 16-bit
- **CPI Range:** (1.0, 4.0)
- **Typical CPI:** 3.5

## Performance

- **Estimated MIPS:** 2.9
- **Typical CPI:** 3.5

## Performance Model

### Usage

```python
from hd63484_2_validated import Hd634842Model

model = Hd634842Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
hd63484_2/
├── README.md                          # This documentation
├── current/
│   └── hd63484_2_validated.py        # Validated model
├── validation/
│   └── hd63484_2_validation.json     # Validation data
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
