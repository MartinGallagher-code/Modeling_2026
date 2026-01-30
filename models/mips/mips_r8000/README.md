# MIPS R8000

## Overview

**MIPS R8000** (1994) - First superscalar MIPS, 4-way FP, scientific workloads

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1994 |
| Manufacturer | MIPS |
| Data Width | 64-bit |
| Clock | 90.0 MHz |
| Transistors | 2,600,000 |
| Technology | 0.5um CMOS |

## Architecture

- **Data Width:** 64-bit
- **CPI Range:** (1.0, 8.0)
- **Typical CPI:** 1.2

## Performance

- **Estimated MIPS:** 75.0
- **Typical CPI:** 1.2

## Performance Model

### Usage

```python
from mips_r8000_validated import MipsR8000Model

model = MipsR8000Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
mips_r8000/
├── README.md                          # This documentation
├── current/
│   └── mips_r8000_validated.py        # Validated model
├── validation/
│   └── mips_r8000_validation.json     # Validation data
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
