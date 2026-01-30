# HP PA-7100

## Overview

**HP PA-7100** (1992) - Second-gen PA-RISC, multimedia instructions

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1992 |
| Manufacturer | HP |
| Data Width | 32-bit |
| Clock | 100.0 MHz |
| Transistors | 850,000 |
| Technology | 0.8um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 12.0)
- **Typical CPI:** 1.2

## Performance

- **Estimated MIPS:** 83.3
- **Typical CPI:** 1.2

## Performance Model

### Usage

```python
from pa7100_validated import Pa7100Model

model = Pa7100Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
pa7100/
├── README.md                          # This documentation
├── current/
│   └── pa7100_validated.py        # Validated model
├── validation/
│   └── pa7100_validation.json     # Validation data
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
