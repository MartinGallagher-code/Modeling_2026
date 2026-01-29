# Intel 8748

## Overview

**Intel 8748** (1977) - EPROM version of 8048

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1977 |
| Manufacturer | Various |
| Data Width | 8-bit |
| Clock | 6.0 MHz |
| Transistors | 8,000 |
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
from i8748_validated import I8748Model

model = I8748Model()
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
i8748/
├── README.md                      # This documentation
├── current/
│   └── i8748_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── i8748_validation.json  # Validation data
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
