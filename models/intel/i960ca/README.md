# Intel i960CA

## Overview

**Intel i960CA** (1989) - Superscalar i960, 3-issue, RAID controller standard

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1989 |
| Manufacturer | Intel |
| Data Width | 32-bit |
| Clock | 33.0 MHz |
| Transistors | 600,000 |
| Technology | 0.8um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 8.0)
- **Typical CPI:** 0.9

## Performance

- **Estimated MIPS:** 36.7
- **Typical CPI:** 0.9

## Performance Model

### Usage

```python
from i960ca_validated import I960caModel

model = I960caModel()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
i960ca/
├── README.md                          # This documentation
├── current/
│   └── i960ca_validated.py        # Validated model
├── validation/
│   └── i960ca_validation.json     # Validation data
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
