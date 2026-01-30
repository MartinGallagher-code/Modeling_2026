# Apollo DN300 PRISM

## Overview

**Apollo DN300 PRISM** (1983) - 68000-derived graphics workstation processor

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1983 |
| Manufacturer | Apollo Computer |
| Data Width | 32-bit |
| Clock | 10.0 MHz |
| Transistors | 100,000 |
| Technology | NMOS |
| Package | PGA |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (2, 10)
- **Typical CPI:** 4.5

## Performance

- **IPS Range:** 1,200,000 - 5,000,000
- **MIPS (estimated):** 1.2 - 5.0
- **Typical CPI:** 4.5

## Performance Model

### Usage

```python
from apollo_dn300_validated import ApolloDN300Model

model = ApolloDN300Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
apollo_dn300/
├── README.md                            # This documentation
├── current/
│   └── apollo_dn300_validated.py        # Validated model (USE THIS)
├── validation/
│   └── apollo_dn300_validation.json     # Validation data
├── docs/                                # Additional documentation
├── CHANGELOG.md                         # Cumulative history
└── HANDOFF.md                           # Current state + next steps
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
