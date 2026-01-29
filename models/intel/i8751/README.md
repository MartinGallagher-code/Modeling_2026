# Intel 8751

## Overview

**Intel 8751** (1983) - EPROM version of 8051

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1983 |
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
from i8751_validated import I8751Model

model = I8751Model()
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
i8751/
├── README.md                      # This documentation
├── current/
│   └── i8751_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── i8751_validation.json  # Validation data
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
