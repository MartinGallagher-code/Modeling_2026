# WDC 65816

## Overview

**WDC 65816** (1984) - SNES CPU, Apple IIGS

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1984 |
| Manufacturer | Various |
| Data Width | 16-bit |
| Clock | 4.0 MHz |
| Transistors | 22,000 |
| Technology | CMOS |
| Package | 40-pin DIP |

## Architecture

- **Data Width:** 16-bit
- **CPI Range:** (2, 8)
- **Typical CPI:** 3.5

## Performance

- **IPS Range:** 800,000 - 1,600,000
- **MIPS (estimated):** 0.800 - 1.600
- **Typical CPI:** 3.5

## Performance Model

### Usage

```python
from wdc65816_validated import WDC65816Model

model = WDC65816Model()
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
wdc65816/
├── README.md                      # This documentation
├── current/
│   └── wdc65816_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── wdc65816_validation.json  # Validation data
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
