# SNK LSPC2-A2

## Overview

**SNK LSPC2-A2** (1990) - Neo Geo video processor, hardware sprite scaler

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1990 |
| Manufacturer | SNK |
| Data Width | 16-bit |
| Clock | 24.0 MHz |
| Transistors | 200,000 |
| Technology | 0.8um CMOS |

## Architecture

- **Data Width:** 16-bit
- **CPI Range:** (1.0, 4.0)
- **Typical CPI:** 2.5

## Performance

- **Estimated MIPS:** 9.6
- **Typical CPI:** 2.5

## Performance Model

### Usage

```python
from snk_lspc2_validated import SnkLspc2Model

model = SnkLspc2Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
snk_lspc2/
├── README.md                          # This documentation
├── current/
│   └── snk_lspc2_validated.py        # Validated model
├── validation/
│   └── snk_lspc2_validation.json     # Validation data
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
