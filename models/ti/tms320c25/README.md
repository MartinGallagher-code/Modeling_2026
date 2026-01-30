# TI TMS320C25

## Overview

**TI TMS320C25** (1986) - 100ns cycle, Harvard architecture, dominant in modems

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1986 |
| Manufacturer | TI |
| Data Width | 16-bit |
| Clock | 40.0 MHz |
| Transistors | 100,000 |
| Technology | 1.0um CMOS |

## Architecture

- **Data Width:** 16-bit
- **CPI Range:** (1.0, 2.0)
- **Typical CPI:** 1.2

## Performance

- **Estimated MIPS:** 33.3
- **Typical CPI:** 1.2

## Performance Model

### Usage

```python
from tms320c25_validated import Tms320c25Model

model = Tms320c25Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
tms320c25/
├── README.md                          # This documentation
├── current/
│   └── tms320c25_validated.py        # Validated model
├── validation/
│   └── tms320c25_validation.json     # Validation data
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
