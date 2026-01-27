# NS32032

## Overview

**NS32032** (1984) - Improved NS32016

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1984 |
| Manufacturer | Various |
| Data Width | 32-bit |
| Clock | 10.0 MHz |
| Transistors | 80,000 |
| Technology | NMOS |
| Package | 84-pin PGA |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (3, 80)
- **Typical CPI:** 10.0

## Performance

- **IPS Range:** 700,000 - 1,500,000
- **MIPS (estimated):** 0.700 - 1.500
- **Typical CPI:** 10.0

## Performance Model

### Usage

```python
from ns32032_validated import NS32032Model

model = NS32032Model()
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
ns32032/
├── README.md                      # This documentation
├── current/
│   └── ns32032_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── ns32032_validation.json  # Validation data
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
