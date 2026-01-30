# Ridge 32

## Overview

**Ridge 32** (1982) - Early RISC-like workstation processor

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1982 |
| Manufacturer | Ridge Computers |
| Data Width | 32-bit |
| Clock | 10.0 MHz |
| Transistors | 50,000 |
| Technology | NMOS |
| Package | DIP |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (2, 8)
- **Typical CPI:** 3.5

## Performance

- **IPS Range:** 1,500,000 - 5,000,000
- **MIPS (estimated):** 1.5 - 5.0
- **Typical CPI:** 3.5

## Performance Model

### Usage

```python
from ridge_32_validated import Ridge32Model

model = Ridge32Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
ridge_32/
├── README.md                          # This documentation
├── current/
│   └── ridge_32_validated.py          # Validated model (USE THIS)
├── validation/
│   └── ridge_32_validation.json       # Validation data
├── docs/                              # Additional documentation
├── CHANGELOG.md                       # Cumulative history
└── HANDOFF.md                         # Current state + next steps
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
