# AT&T DSP32C

## Overview

**AT&T DSP32C** (1988) - 32-bit floating-point, 50 MIPS, Bell Labs telecom

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1988 |
| Manufacturer | AT&T |
| Data Width | 32-bit |
| Clock | 50.0 MHz |
| Transistors | 300,000 |
| Technology | 0.8um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 2.0)
- **Typical CPI:** 1.1

## Performance

- **Estimated MIPS:** 45.5
- **Typical CPI:** 1.1

## Performance Model

### Usage

```python
from att_dsp32c_validated import AttDsp32cModel

model = AttDsp32cModel()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
att_dsp32c/
├── README.md                          # This documentation
├── current/
│   └── att_dsp32c_validated.py        # Validated model
├── validation/
│   └── att_dsp32c_validation.json     # Validation data
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
