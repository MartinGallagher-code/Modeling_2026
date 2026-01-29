# Intel 8088

## Overview

**Intel 8088** (1979) - 8-bit bus version, IBM PC CPU

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1979 |
| Manufacturer | Various |
| Data Width | 16-bit |
| Clock | 5.0 MHz |
| Transistors | 29,000 |
| Technology | 3µm NMOS |
| Package | 40-pin DIP |

## Architecture

- **Data Width:** 16-bit
- **CPI Range:** (2, 200)
- **Typical CPI:** 15.0

## Performance

- **IPS Range:** 250,000 - 500,000
- **MIPS (estimated):** 0.250 - 0.500
- **Typical CPI:** 15.0

## Performance Model

### Usage

```python
from i8088_validated import I8088Model

model = I8088Model()
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
i8088/
├── README.md                      # This documentation
├── current/
│   └── i8088_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── i8088_validation.json  # Validation data
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
