# AMD Am79C970 PCnet

## Overview

**AMD Am79C970 PCnet** (1993) - Ethernet controller with on-chip processor

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1993 |
| Manufacturer | AMD |
| Data Width | 32-bit |
| Clock | 20.0 MHz |
| Transistors | 200,000 |
| Technology | 0.6um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 4.0)
- **Typical CPI:** 2.5

## Performance

- **Estimated MIPS:** 8.0
- **Typical CPI:** 2.5

## Performance Model

### Usage

```python
from am79c970_validated import Am79c970Model

model = Am79c970Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
am79c970/
├── README.md                          # This documentation
├── current/
│   └── am79c970_validated.py        # Validated model
├── validation/
│   └── am79c970_validation.json     # Validation data
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
