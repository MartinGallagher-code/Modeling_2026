# Hitachi SH-1

## Overview

**Hitachi SH-1** (1992) - 32-bit RISC for embedded, 16-bit compressed ISA

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1992 |
| Manufacturer | Hitachi |
| Data Width | 32-bit |
| Clock | 20.0 MHz |
| Transistors | 400,000 |
| Technology | 0.8um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 10.0)
- **Typical CPI:** 1.4

## Performance

- **Estimated MIPS:** 14.3
- **Typical CPI:** 1.4

## Performance Model

### Usage

```python
from sh1_validated import Sh1Model

model = Sh1Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
sh1/
├── README.md                          # This documentation
├── current/
│   └── sh1_validated.py        # Validated model
├── validation/
│   └── sh1_validation.json     # Validation data
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
