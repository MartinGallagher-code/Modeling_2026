# Sequoia S-16

## Overview

**Sequoia S-16** (1983) - Fault-tolerant processor with checkpoint/recovery

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1983 |
| Manufacturer | Sequoia Systems |
| Data Width | 16/32-bit |
| Clock | 8.0 MHz |
| Transistors | 60,000 |
| Technology | CMOS |
| Package | PGA |

## Architecture

- **Data Width:** 16/32-bit
- **CPI Range:** (3, 12)
- **Typical CPI:** 5.0

## Performance

- **IPS Range:** 800,000 - 2,700,000
- **MIPS (estimated):** 0.8 - 2.7
- **Typical CPI:** 5.0

## Performance Model

### Usage

```python
from sequoia_s16_validated import SequoiaS16Model

model = SequoiaS16Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.3f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Directory Structure

```
sequoia_s16/
├── README.md                            # This documentation
├── current/
│   └── sequoia_s16_validated.py         # Validated model (USE THIS)
├── validation/
│   └── sequoia_s16_validation.json      # Validation data
├── docs/                                # Additional documentation
├── CHANGELOG.md                         # Cumulative history
└── HANDOFF.md                           # Current state + next steps
```

## Validation

| Test | Status |
|------|--------|
| CPI Target | PASSED (0.04% error) |
| IPS Range | Validated against specifications |
| Architecture | Cross-referenced with datasheets |

**Target Accuracy:** <5% CPI prediction error

---

*Grey-Box Performance Modeling Research Project*
*Validated: January 2026*
