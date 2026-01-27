# TI TMS9900

## Overview

**TI TMS9900** (1976) - Memory-to-memory architecture

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1976 |
| Manufacturer | Various |
| Data Width | 16-bit |
| Clock | 3.0 MHz |
| Transistors | 8,000 |
| Technology | NMOS |
| Package | 64-pin DIP |

## Architecture

- **Data Width:** 16-bit
- **CPI Range:** (8, 64)
- **Typical CPI:** 20.0

## Performance

- **IPS Range:** 100,000 - 300,000
- **MIPS (estimated):** 0.100 - 0.300
- **Typical CPI:** 20.0

## Performance Model

### Usage

```python
from tms9900_validated import TMS9900Model

model = TMS9900Model()
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
tms9900/
├── README.md                      # This documentation
├── current/
│   └── tms9900_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── tms9900_validation.json  # Validation data
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
