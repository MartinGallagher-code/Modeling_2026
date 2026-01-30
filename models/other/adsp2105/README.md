# Analog Devices ADSP-2105

## Overview

**Analog Devices ADSP-2105** (1992) - Low-cost fixed-point DSP, consumer audio

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1992 |
| Manufacturer | Analog Devices |
| Data Width | 16-bit |
| Clock | 20.0 MHz |
| Transistors | 200,000 |
| Technology | 0.6um CMOS |

## Architecture

- **Data Width:** 16-bit
- **CPI Range:** (1.0, 3.0)
- **Typical CPI:** 1.3

## Performance

- **Estimated MIPS:** 15.4
- **Typical CPI:** 1.3

## Performance Model

### Usage

```python
from adsp2105_validated import Adsp2105Model

model = Adsp2105Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
adsp2105/
├── README.md                          # This documentation
├── current/
│   └── adsp2105_validated.py        # Validated model
├── validation/
│   └── adsp2105_validation.json     # Validation data
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
