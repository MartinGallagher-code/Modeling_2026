# Fairchild F8

## Overview

**Fairchild F8** (1975) - First single-chip MCU design

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1975 |
| Manufacturer | Various |
| Data Width | 8-bit |
| Clock | 2.0 MHz |
| Transistors | 5,000 |
| Technology | NMOS |
| Package | 40-pin DIP |

## Architecture

- **Data Width:** 8-bit
- **CPI Range:** (4, 20)
- **Typical CPI:** 7.0

## Performance

- **IPS Range:** 200,000 - 450,000
- **MIPS (estimated):** 0.200 - 0.450
- **Typical CPI:** 7.0

## Performance Model

### Usage

```python
from f8_validated import F8Model

model = F8Model()
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
f8/
├── README.md                      # This documentation
├── current/
│   └── f8_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── f8_validation.json  # Validation data
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
