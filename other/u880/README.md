# East German U880

## Overview

**U880** (1980) - Z80 clone by VEB Mikroelektronik Erfurt (East Germany)

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1980 |
| Manufacturer | VEB Mikroelektronik Erfurt |
| Data Width | 8-bit |
| Clock | 2.5 MHz |
| Transistors | 8,500 |
| Technology | NMOS |
| Package | 40-pin DIP |

## Architecture

- **Type:** 8-bit microprocessor (Z80 clone)
- **Instruction Set:** Full Z80 compatibility
- **Timing:** Identical to Zilog Z80
- **CPI Range:** 4-23 cycles per instruction
- **Typical CPI:** 5.5

## Historical Context

The U880 was manufactured by VEB Mikroelektronik Erfurt in the German Democratic Republic (East Germany). It is a pin-compatible, timing-compatible clone of the Zilog Z80. Used in:

- KC 85 series home computers
- Robotron computers
- Various Eastern Bloc computing systems

## Performance

- **IPS Range:** 200,000 - 625,000
- **MIPS (estimated):** 0.45
- **Typical CPI:** 5.5 (identical to Z80)

## Performance Model

### Usage

```python
from u880_validated import U880Model

model = U880Model()
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
u880/
├── README.md                      # This documentation
├── HANDOFF.md                     # Handoff notes
├── CHANGELOG.md                   # Change history
├── __init__.py                    # Module init
├── current/
│   └── u880_validated.py          # Validated model (USE THIS)
└── validation/
    └── u880_validation.json       # Validation data
```

## Validation

| Test | Status |
|------|--------|
| CPI Accuracy | Validated (5.5, identical to Z80) |
| Weight Sums | All workloads sum to 1.0 |
| Cycle Ranges | All within expected bounds |

**Target Accuracy:** +/-5% for performance estimates

---

*Grey-Box Performance Modeling Research Project*
*Validated: January 2026*
