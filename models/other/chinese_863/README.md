# Chinese 863 Program CPU

## Overview

**Chinese 863 Program CPU** (1990) - Early Chinese CPU R&D, reverse-engineered Z80/8086 cores

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1990 |
| Manufacturer | ICTS |
| Data Width | 16-bit |
| Clock | 8.0 MHz |
| Transistors | 100,000 |
| Technology | 2.0um CMOS |

## Architecture

- **Data Width:** 16-bit
- **CPI Range:** (3.0, 30.0)
- **Typical CPI:** 4.5

## Performance

- **Estimated MIPS:** 1.8
- **Typical CPI:** 4.5

## Performance Model

### Usage

```python
from chinese_863_validated import Chinese863Model

model = Chinese863Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
chinese_863/
├── README.md                          # This documentation
├── current/
│   └── chinese_863_validated.py        # Validated model
├── validation/
│   └── chinese_863_validation.json     # Validation data
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
