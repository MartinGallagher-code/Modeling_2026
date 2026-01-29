# AMD Am2903

## Overview

**AMD Am2903** (1976) - Enhanced Am2901 with multiply

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1976 |
| Manufacturer | Various |
| Data Width | 4-bit |
| Clock | 10.0 MHz |
| Transistors | 400 |
| Technology | Bipolar |
| Package | 48-pin DIP |

## Architecture

- **Data Width:** 4-bit
- **CPI Range:** (1, 1)
- **Typical CPI:** 1.0

## Performance

- **IPS Range:** 2,500,000 - 10,000,000
- **MIPS (estimated):** 2.500 - 10.000
- **Typical CPI:** 1.0

## Performance Model

### Usage

```python
from am2903_validated import AM2903Model

model = AM2903Model()
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
am2903/
├── README.md                      # This documentation
├── current/
│   └── am2903_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── am2903_validation.json  # Validation data
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
