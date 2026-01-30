# MIPS R4000

## Overview

**MIPS R4000** (1991) - First commercial 64-bit RISC, 8-stage superpipeline

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1991 |
| Manufacturer | MIPS |
| Data Width | 64-bit |
| Clock | 100.0 MHz |
| Transistors | 1,350,000 |
| Technology | 0.8um CMOS |

## Architecture

- **Data Width:** 64-bit
- **CPI Range:** (1.0, 15.0)
- **Typical CPI:** 1.5

## Performance

- **Estimated MIPS:** 66.7
- **Typical CPI:** 1.5

## Performance Model

### Usage

```python
from mips_r4000_validated import MipsR4000Model

model = MipsR4000Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
mips_r4000/
├── README.md                          # This documentation
├── current/
│   └── mips_r4000_validated.py        # Validated model
├── validation/
│   └── mips_r4000_validation.json     # Validation data
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
