# Intel i82596

## Overview

**Intel i82596** (1987) - 32-bit Ethernet coprocessor, TCP offload

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1987 |
| Manufacturer | Intel |
| Data Width | 32-bit |
| Clock | 16.0 MHz |
| Transistors | 120,000 |
| Technology | 1.0um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 4.0)
- **Typical CPI:** 3.0

## Performance

- **Estimated MIPS:** 5.3
- **Typical CPI:** 3.0

## Performance Model

### Usage

```python
from i82596_validated import I82596Model

model = I82596Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
i82596/
├── README.md                          # This documentation
├── current/
│   └── i82596_validated.py        # Validated model
├── validation/
│   └── i82596_validation.json     # Validation data
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
