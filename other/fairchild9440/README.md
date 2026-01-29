# Fairchild 9440 MICROFLAME

## Overview

**Fairchild 9440 MICROFLAME** (1979) - Data General Nova ISA on a single chip

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1979 |
| Manufacturer | Fairchild Semiconductor |
| Data Width | 16-bit |
| Clock | 10.0 MHz |
| Transistors | ~5,000 |
| Technology | I2L (Bipolar) |
| Package | 40-pin DIP |

## Architecture

- **Type:** 16-bit minicomputer-on-a-chip
- **ISA:** Data General Nova compatible
- **Accumulators:** 4 (AC0-AC3)
- **Address Space:** 32K words (15-bit)
- **CPI Range:** 2-6 cycles per instruction
- **Typical CPI:** 3.5

## Historical Context

The Fairchild 9440 implemented the Data General Nova instruction set on a single chip using I2L (Integrated Injection Logic) bipolar technology. It was faster than the original Nova minicomputer, demonstrating that single-chip implementations could exceed discrete-logic performance.

## Performance

- **IPS Range:** 1,666,667 - 5,000,000
- **MIPS (estimated):** 2.86
- **Typical CPI:** 3.5

## Performance Model

### Usage

```python
from fairchild9440_validated import Fairchild9440Model

model = Fairchild9440Model()
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
fairchild9440/
├── README.md                            # This documentation
├── HANDOFF.md                           # Handoff notes
├── CHANGELOG.md                         # Change history
├── __init__.py                          # Module init
├── current/
│   └── fairchild9440_validated.py       # Validated model (USE THIS)
└── validation/
    └── fairchild9440_validation.json    # Validation data
```

## Validation

| Test | Status |
|------|--------|
| CPI Accuracy | Validated (3.5 target) |
| Weight Sums | All workloads sum to 1.0 |
| Cycle Ranges | All within expected bounds |

**Target Accuracy:** +/-5% for performance estimates

---

*Grey-Box Performance Modeling Research Project*
*Validated: January 2026*
