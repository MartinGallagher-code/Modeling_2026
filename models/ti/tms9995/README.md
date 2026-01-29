# TI TMS9995

## Overview

**TI TMS9995** (1981) - Improved TMS9900

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1981 |
| Manufacturer | Various |
| Data Width | 16-bit |
| Clock | 12.0 MHz |
| Transistors | 20,000 |
| Technology | NMOS |
| Package | 40-pin DIP |

## Architecture

- **Data Width:** 16-bit
- **CPI Range:** (4, 50)
- **Typical CPI:** 12.0

## Performance

- **IPS Range:** 600,000 - 1,500,000
- **MIPS (estimated):** 0.600 - 1.500
- **Typical CPI:** 12.0

## Performance Model

### Usage

```python
from tms9995_validated import TMS9995Model

model = TMS9995Model()
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
tms9995/
├── README.md                      # This documentation
├── current/
│   └── tms9995_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── tms9995_validation.json  # Validation data
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
