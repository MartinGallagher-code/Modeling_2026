# Tseng Labs ET4000

## Overview

**Tseng Labs ET4000** (1989) - Fast SVGA with hardware acceleration

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1989 |
| Manufacturer | Tseng Labs |
| Data Width | 32-bit |
| Clock | 40.0 MHz |
| Transistors | 250,000 |
| Technology | 0.8um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 3.0)
- **Typical CPI:** 2.5

## Performance

- **Estimated MIPS:** 16.0
- **Typical CPI:** 2.5

## Performance Model

### Usage

```python
from et4000_validated import Et4000Model

model = Et4000Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
et4000/
├── README.md                          # This documentation
├── current/
│   └── et4000_validated.py        # Validated model
├── validation/
│   └── et4000_validation.json     # Validation data
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
