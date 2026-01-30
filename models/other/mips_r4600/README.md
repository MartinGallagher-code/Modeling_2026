# MIPS R4600 Orion

## Overview

**MIPS R4600 Orion** (1994) - Low-cost R4000 derivative, Cisco routers

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1994 |
| Manufacturer | QED/IDT |
| Data Width | 64-bit |
| Clock | 133.0 MHz |
| Transistors | 1,900,000 |
| Technology | 0.64um CMOS |

## Architecture

- **Data Width:** 64-bit
- **CPI Range:** (1.0, 12.0)
- **Typical CPI:** 1.3

## Performance

- **Estimated MIPS:** 102.3
- **Typical CPI:** 1.3

## Performance Model

### Usage

```python
from mips_r4600_validated import MipsR4600Model

model = MipsR4600Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
mips_r4600/
├── README.md                          # This documentation
├── current/
│   └── mips_r4600_validated.py        # Validated model
├── validation/
│   └── mips_r4600_validation.json     # Validation data
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
