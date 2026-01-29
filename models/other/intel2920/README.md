# Intel 2920

## Overview

**Intel 2920** (1979) - First Intel analog signal processor (DSP)

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1979 |
| Manufacturer | Intel |
| Data Width | 25-bit |
| Clock | 5.0 MHz |
| Transistors | ~15,000 |
| Technology | NMOS |
| Package | 40-pin DIP |

## Architecture

- **Type:** Analog signal processor (first Intel DSP attempt)
- **On-chip:** ADC (8-bit), DAC (8-bit)
- **NO hardware multiplier**
- **Program ROM:** 192 x 24-bit words
- **Data RAM:** 40 x 25-bit words
- **CPI Range:** 2-4 cycles per instruction (400-800ns)
- **Typical CPI:** 5.0 (DSP workloads with software MAC)

## Performance

- **IPS Range:** 800,000 - 2,500,000
- **MIPS (estimated):** 1.0
- **Typical CPI:** 5.0

## Performance Model

### Usage

```python
from intel2920_validated import Intel2920Model

model = Intel2920Model()
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
intel2920/
├── README.md                          # This documentation
├── HANDOFF.md                         # Handoff notes
├── CHANGELOG.md                       # Change history
├── __init__.py                        # Module init
├── current/
│   └── intel2920_validated.py         # Validated model (USE THIS)
└── validation/
    └── intel2920_validation.json      # Validation data
```

## Validation

| Test | Status |
|------|--------|
| CPI Accuracy | Validated (5.0 target) |
| Weight Sums | All workloads sum to 1.0 |
| Cycle Ranges | All within expected bounds |

**Target Accuracy:** +/-5% for performance estimates

---

*Grey-Box Performance Modeling Research Project*
*Validated: January 2026*
