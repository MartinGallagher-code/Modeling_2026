# Fairchild Clipper C100

## Overview

**Clipper C100** (1985) - Fairchild RISC processor

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1985 |
| Manufacturer | Fairchild |
| Data Width | 32-bit |
| Clock | 33.0 MHz |
| Transistors | 132,000 |
| Technology | CMOS |
| Package | PGA |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1, 3)
- **Typical CPI:** 1.5

## Performance

- **IPS Range:** 15,000,000 - 33,000,000
- **MIPS (estimated):** 15.0 - 33.0
- **Typical CPI:** 1.5

## Performance Model

### Usage

```python
from clipper_c100_validated import ClipperC100Model

model = ClipperC100Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
clipper_c100/
├── README.md                            # This documentation
├── current/
│   └── clipper_c100_validated.py        # Validated model (USE THIS)
├── validation/
│   └── clipper_c100_validation.json     # Validation data
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
