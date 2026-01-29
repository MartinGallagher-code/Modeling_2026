# Fujitsu MB8841

## Overview

**Fujitsu MB8841** (1977) - 4-bit MCU used in Namco arcade games

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1977 |
| Manufacturer | Fujitsu |
| Data Width | 4-bit |
| Clock | 1.0 MHz |
| Transistors | ~3,000 |
| Technology | NMOS |
| Package | 42-pin DIP |

## Architecture

- **Type:** 4-bit microcontroller (Harvard architecture)
- **ROM:** 1KB program memory
- **RAM:** 32 nibbles data memory
- **Instructions:** 64
- **CPI Range:** 3-8 cycles per instruction
- **Typical CPI:** 4.0

## Notable Uses

- Namco Galaga (1981) - uses 3x MB8841 chips
- Namco Xevious (1982)
- Namco Bosconian (1981)

## Performance

- **IPS Range:** 125,000 - 333,333
- **MIPS (estimated):** 0.25
- **Typical CPI:** 4.0

## Performance Model

### Usage

```python
from mb8841_validated import MB8841Model

model = MB8841Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"Bottleneck: {result.bottleneck}")

validation = model.validate()
for test in validation['tests']:
    status = "PASS" if test['passed'] else "FAIL"
    print(f"{test['name']}: {status}")
```

## Directory Structure

```
mb8841/
├── README.md                        # This documentation
├── HANDOFF.md                       # Handoff notes
├── CHANGELOG.md                     # Change history
├── __init__.py                      # Module init
├── current/
│   └── mb8841_validated.py          # Validated model (USE THIS)
└── validation/
    └── mb8841_validation.json       # Validation data
```

## Validation

| Test | Status |
|------|--------|
| CPI Accuracy | Validated (4.0 target) |
| Weight Sums | All workloads sum to 1.0 |
| Cycle Ranges | All within expected bounds |

**Target Accuracy:** +/-5% for performance estimates

---

*Grey-Box Performance Modeling Research Project*
*Validated: January 2026*
