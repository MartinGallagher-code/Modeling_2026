# NEC uPD7759

## Overview

**NEC uPD7759** (1987) - ADPCM voice synthesis for arcade games

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1987 |
| Manufacturer | NEC |
| Data Width | 8-bit |
| Clock | 5.0 MHz |
| Transistors | 80,000 |
| Technology | 1.0um CMOS |

## Architecture

- **Data Width:** 8-bit
- **CPI Range:** (1.0, 3.0)
- **Typical CPI:** 3.0

## Performance

- **Estimated MIPS:** 1.7
- **Typical CPI:** 3.0

## Performance Model

### Usage

```python
from upd7759_validated import Upd7759Model

model = Upd7759Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
upd7759/
├── README.md                          # This documentation
├── current/
│   └── upd7759_validated.py        # Validated model
├── validation/
│   └── upd7759_validation.json     # Validation data
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
