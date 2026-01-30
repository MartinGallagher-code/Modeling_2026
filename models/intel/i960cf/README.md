# Intel i960CF

## Overview

**Intel i960CF** (1992) - Enhanced i960 with on-chip FPU

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1992 |
| Manufacturer | Intel |
| Data Width | 32-bit |
| Clock | 33.0 MHz |
| Transistors | 900,000 |
| Technology | 0.6um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 8.0)
- **Typical CPI:** 0.85

## Performance

- **Estimated MIPS:** 38.8
- **Typical CPI:** 0.85

## Performance Model

### Usage

```python
from i960cf_validated import I960cfModel

model = I960cfModel()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
i960cf/
├── README.md                          # This documentation
├── current/
│   └── i960cf_validated.py        # Validated model
├── validation/
│   └── i960cf_validation.json     # Validation data
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
