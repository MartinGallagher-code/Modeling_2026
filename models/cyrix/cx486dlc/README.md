# Cyrix Cx486DLC

## Overview

**Cyrix Cx486DLC** (1992) - 486 ISA in 386 pin-out, 1KB cache

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1992 |
| Manufacturer | Cyrix |
| Data Width | 32-bit |
| Clock | 33.0 MHz |
| Transistors | 600,000 |
| Technology | 0.8um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.5, 30.0)
- **Typical CPI:** 2.5

## Performance

- **Estimated MIPS:** 13.2
- **Typical CPI:** 2.5

## Performance Model

### Usage

```python
from cx486dlc_validated import Cx486dlcModel

model = Cx486dlcModel()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
cx486dlc/
├── README.md                          # This documentation
├── current/
│   └── cx486dlc_validated.py        # Validated model
├── validation/
│   └── cx486dlc_validation.json     # Validation data
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
