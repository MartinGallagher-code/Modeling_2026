# Cypress CY7C601

## Overview

**Cypress CY7C601** (1988) - Early merchant SPARC, 25-40 MHz

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1988 |
| Manufacturer | Cypress |
| Data Width | 32-bit |
| Clock | 40.0 MHz |
| Transistors | 250,000 |
| Technology | 0.8um CMOS |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1.0, 16.0)
- **Typical CPI:** 1.6

## Performance

- **Estimated MIPS:** 25.0
- **Typical CPI:** 1.6

## Performance Model

### Usage

```python
from cy7c601_validated import Cy7c601Model

model = Cy7c601Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
cy7c601/
├── README.md                          # This documentation
├── current/
│   └── cy7c601_validated.py        # Validated model
├── validation/
│   └── cy7c601_validation.json     # Validation data
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
