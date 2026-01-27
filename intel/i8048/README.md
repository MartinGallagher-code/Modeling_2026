# Intel 8048

## Overview

**Intel 8048** (1976) - First single-chip microcontroller

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1976 |
| Manufacturer | Various |
| Data Width | 8-bit |
| Clock | 6.0 MHz |
| Transistors | 6,000 |
| Technology | NMOS |
| Package | 40-pin DIP |

## Architecture

- **Data Width:** 8-bit
- **CPI Range:** (1, 2)
- **Typical CPI:** 1.5

## Performance

- **IPS Range:** 400,000 - 500,000
- **MIPS (estimated):** 0.400 - 0.500
- **Typical CPI:** 1.5

## Performance Model

### Usage

```python
from i8048_validated import I8048Model

model = I8048Model()
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
i8048/
├── README.md                      # This documentation
├── current/
│   └── i8048_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── i8048_validation.json  # Validation data
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
