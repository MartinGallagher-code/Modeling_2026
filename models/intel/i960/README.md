# Intel i960

## Overview

**Intel i960** (1988) - 32-bit embedded RISC, register scoreboarding

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1988 |
| Manufacturer | Intel |
| Data Width | 32-bit |
| Clock | 33.0 MHz |
| Transistors | 250,000 |
| Technology | 1.0um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 10.0)
- **Typical CPI:** 1.5

## Performance

- **Estimated MIPS:** 22.0
- **Typical CPI:** 1.5

## Performance Model

### Usage

```python
from i960_validated import I960Model

model = I960Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
i960/
├── README.md                          # This documentation
├── current/
│   └── i960_validated.py        # Validated model
├── validation/
│   └── i960_validation.json     # Validation data
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
