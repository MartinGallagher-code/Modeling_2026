# Intel 8085

## Overview

**Intel 8085** (1976) - Enhanced 8080, single +5V supply

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1976 |
| Manufacturer | Various |
| Data Width | 8-bit |
| Clock | 3.0 MHz |
| Transistors | 6,500 |
| Technology | 3µm NMOS |
| Package | 40-pin DIP |

## Architecture

- **Data Width:** 8-bit
- **CPI Range:** (4, 18)
- **Typical CPI:** 6.5

## Performance

- **IPS Range:** 370,000 - 769,000
- **MIPS (estimated):** 0.370 - 0.769
- **Typical CPI:** 6.5

## Performance Model

### Usage

```python
from i8085_validated import I8085Model

model = I8085Model()
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
i8085/
├── README.md                      # This documentation
├── current/
│   └── i8085_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── i8085_validation.json  # Validation data
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
