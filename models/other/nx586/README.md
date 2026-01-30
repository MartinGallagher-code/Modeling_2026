# NexGen Nx586

## Overview

**NexGen Nx586** (1994) - x86-compatible RISC core with x86 translation

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1994 |
| Manufacturer | NexGen |
| Data Width | 32-bit |
| Clock | 93.0 MHz |
| Transistors | 3,500,000 |
| Technology | 0.44um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 15.0)
- **Typical CPI:** 1.3

## Performance

- **Estimated MIPS:** 71.5
- **Typical CPI:** 1.3

## Performance Model

### Usage

```python
from nx586_validated import Nx586Model

model = Nx586Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
nx586/
├── README.md                          # This documentation
├── current/
│   └── nx586_validated.py        # Validated model
├── validation/
│   └── nx586_validation.json     # Validation data
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
