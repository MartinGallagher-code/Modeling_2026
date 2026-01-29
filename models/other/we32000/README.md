# WE 32000

## Overview

**WE 32000** (1982) - AT&T UNIX workstation CPU

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1982 |
| Manufacturer | Various |
| Data Width | 32-bit |
| Clock | 14.0 MHz |
| Transistors | 120,000 |
| Technology | CMOS |
| Package | 68-pin PGA |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (3, 50)
- **Typical CPI:** 8.0

## Performance

- **IPS Range:** 1,200,000 - 3,000,000
- **MIPS (estimated):** 1.200 - 3.000
- **Typical CPI:** 8.0

## Performance Model

### Usage

```python
from we32000_validated import WE32000Model

model = WE32000Model()
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
we32000/
├── README.md                      # This documentation
├── current/
│   └── we32000_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── we32000_validation.json  # Validation data
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
