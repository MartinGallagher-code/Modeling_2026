# AMD Am386

## Overview

**AMD Am386** (1991) - AMD's 386 clone, 40 MHz (faster than Intel's 33 MHz)

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1991 |
| Manufacturer | AMD |
| Data Width | 32-bit |
| Clock | 40.0 MHz |
| Transistors | 275,000 |
| Technology | 1.0um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (2.0, 38.0)
- **Typical CPI:** 4.0

## Performance

- **Estimated MIPS:** 10.0
- **Typical CPI:** 4.0

## Performance Model

### Usage

```python
from am386_validated import Am386Model

model = Am386Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
am386/
├── README.md                          # This documentation
├── current/
│   └── am386_validated.py        # Validated model
├── validation/
│   └── am386_validation.json     # Validation data
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
