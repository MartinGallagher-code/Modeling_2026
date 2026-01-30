# AT&T DSP16

## Overview

**AT&T DSP16** (1987) - 16-bit fixed-point, low-power, modems/voice

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1987 |
| Manufacturer | AT&T |
| Data Width | 16-bit |
| Clock | 25.0 MHz |
| Transistors | 150,000 |
| Technology | 1.0um CMOS |

## Architecture

- **Data Width:** 16-bit
- **CPI Range:** (1.0, 3.0)
- **Typical CPI:** 1.3

## Performance

- **Estimated MIPS:** 19.2
- **Typical CPI:** 1.3

## Performance Model

### Usage

```python
from att_dsp16_validated import AttDsp16Model

model = AttDsp16Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
att_dsp16/
├── README.md                          # This documentation
├── current/
│   └── att_dsp16_validated.py        # Validated model
├── validation/
│   └── att_dsp16_validation.json     # Validation data
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
