# INMOS T414

## Overview

**INMOS T414** (1985) - Transputer with links

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1985 |
| Manufacturer | Various |
| Data Width | 32-bit |
| Clock | 15.0 MHz |
| Transistors | 200,000 |
| Technology | 1.5µm CMOS |
| Package | 84-pin PLCC |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1, 10)
- **Typical CPI:** 2.0

## Performance

- **IPS Range:** 5,000,000 - 10,000,000
- **MIPS (estimated):** 5.000 - 10.000
- **Typical CPI:** 2.0

## Performance Model

### Usage

```python
from t414_validated import T414Model

model = T414Model()
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
t414/
├── README.md                      # This documentation
├── current/
│   └── t414_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── t414_validation.json  # Validation data
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
