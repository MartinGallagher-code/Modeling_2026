# Zilog Z8

## Overview

**Zilog Z8** (1979) - Single-chip MCU

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1979 |
| Manufacturer | Various |
| Data Width | 8-bit |
| Clock | 8.0 MHz |
| Transistors | 12,000 |
| Technology | NMOS |
| Package | 40-pin DIP |

## Architecture

- **Data Width:** 8-bit
- **CPI Range:** (6, 20)
- **Typical CPI:** 10.0

## Performance

- **IPS Range:** 500,000 - 1,300,000
- **MIPS (estimated):** 0.500 - 1.300
- **Typical CPI:** 10.0

## Performance Model

### Usage

```python
from z8_validated import Z8Model

model = Z8Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"MIPS: {result.mips:.3f}")
print(f"Bottleneck: {result.bottleneck}")

# Validate against known specifications
for test, data in model.validate().items():
    status = "✓ PASS" if data['pass'] else "✗ FAIL"
    print(f"{test}: {status}")
```

## Directory Structure

```
z8/
├── README.md                      # This documentation
├── current/
│   └── z8_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── z8_validation.json  # Validation data
└── docs/                          # Additional documentation
```

## Validation

| Test | Status |
|------|--------|
| IPS Range | ✓ Validated against specifications |
| CPI | ✓ Calibrated to workload mix |
| Architecture | ✓ Cross-referenced with datasheets |

**Target Accuracy:** ±15% for performance estimates

---

*Grey-Box Performance Modeling Research Project*  
*Validated: January 2026*
