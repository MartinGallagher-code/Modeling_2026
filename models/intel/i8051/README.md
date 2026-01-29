# Intel 8051

## Overview

**Intel 8051** (1980) - Most successful microcontroller family

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1980 |
| Manufacturer | Various |
| Data Width | 8-bit |
| Clock | 12.0 MHz |
| Transistors | 60,000 |
| Technology | NMOS |
| Package | 40-pin DIP |

## Architecture

- **Data Width:** 8-bit
- **CPI Range:** (12, 24)
- **Typical CPI:** 12.0

## Performance

- **IPS Range:** 500,000 - 1,000,000
- **MIPS (estimated):** 0.500 - 1.000
- **Typical CPI:** 12.0

## Performance Model

### Usage

```python
from i8051_validated import I8051Model

model = I8051Model()
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
i8051/
├── README.md                      # This documentation
├── current/
│   └── i8051_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── i8051_validation.json  # Validation data
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
