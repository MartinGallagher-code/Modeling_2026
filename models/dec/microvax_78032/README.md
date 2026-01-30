# MicroVAX 78032

## Overview

**MicroVAX 78032** (1984) - DEC's first single-chip VAX processor

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1984 |
| Manufacturer | DEC |
| Data Width | 32-bit |
| Clock | 5.0 MHz |
| Transistors | 125,000 |
| Technology | CMOS |
| Package | 68-pin CERDIP |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (2, 15)
- **Typical CPI:** 5.5

## Performance

- **IPS Range:** 500,000 - 1,200,000
- **MIPS (estimated):** 0.500 - 1.200
- **Typical CPI:** 5.5

## Performance Model

### Usage

```python
from microvax_78032_validated import MicroVAX78032Model

model = MicroVAX78032Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
microvax_78032/
├── README.md                              # This documentation
├── current/
│   └── microvax_78032_validated.py        # Validated model (USE THIS)
├── validation/
│   └── microvax_78032_validation.json     # Validation data
├── docs/                                  # Additional documentation
├── CHANGELOG.md                           # Cumulative history
└── HANDOFF.md                             # Current state + next steps
```

## Validation

| Test | Status |
|------|--------|
| CPI Target | PASSED (0.0% error) |
| IPS Range | Validated against specifications |
| Architecture | Cross-referenced with datasheets |

**Target Accuracy:** <5% CPI prediction error

---

*Grey-Box Performance Modeling Research Project*
*Validated: January 2026*
