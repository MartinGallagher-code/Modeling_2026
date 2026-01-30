# MIPS R3000

## Overview

**MIPS R3000** (1988) - 32-bit RISC, 5-stage pipeline, SGI/DECstation, PS1 variant

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1988 |
| Manufacturer | MIPS |
| Data Width | 32-bit |
| Clock | 33.0 MHz |
| Transistors | 120,000 |
| Technology | 1.2um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 12.0)
- **Typical CPI:** 1.4

## Performance

- **Estimated MIPS:** 23.6
- **Typical CPI:** 1.4

## Performance Model

### Usage

```python
from mips_r3000_validated import MipsR3000Model

model = MipsR3000Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
mips_r3000/
├── README.md                          # This documentation
├── current/
│   └── mips_r3000_validated.py        # Validated model
├── validation/
│   └── mips_r3000_validation.json     # Validation data
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
