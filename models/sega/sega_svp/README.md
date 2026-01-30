# Sega SVP (SSP1601)

## Overview

**Sega SVP (SSP1601)** (1994) - DSP in Virtua Racing cartridge

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1994 |
| Manufacturer | Samsung |
| Data Width | 16-bit |
| Clock | 23.0 MHz |
| Transistors | 100,000 |
| Technology | 0.6um CMOS |

## Architecture

- **Data Width:** 16-bit
- **CPI Range:** (1.0, 3.0)
- **Typical CPI:** 1.5

## Performance

- **Estimated MIPS:** 15.3
- **Typical CPI:** 1.5

## Performance Model

### Usage

```python
from sega_svp_validated import SegaSvpModel

model = SegaSvpModel()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
sega_svp/
├── README.md                          # This documentation
├── current/
│   └── sega_svp_validated.py        # Validated model
├── validation/
│   └── sega_svp_validation.json     # Validation data
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
