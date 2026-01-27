# Harris RTX2000

## Overview

**Harris RTX2000** (1988) - Forth stack machine

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1988 |
| Manufacturer | Various |
| Data Width | 16-bit |
| Clock | 10.0 MHz |
| Transistors | 12,000 |
| Technology | CMOS |
| Package | 84-pin PGA |

## Architecture

- **Data Width:** 16-bit
- **CPI Range:** (1, 2)
- **Typical CPI:** 1.1

## Performance

- **IPS Range:** 7,000,000 - 10,000,000
- **MIPS (estimated):** 7.000 - 10.000
- **Typical CPI:** 1.1

## Performance Model

### Usage

```python
from rtx2000_validated import RTX2000Model

model = RTX2000Model()
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
rtx2000/
├── README.md                      # This documentation
├── current/
│   └── rtx2000_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── rtx2000_validation.json  # Validation data
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
