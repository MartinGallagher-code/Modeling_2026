# WDC 65C02

## Overview

**WDC 65C02** (1983) - CMOS 6502 with bug fixes

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1983 |
| Manufacturer | Various |
| Data Width | 8-bit |
| Clock | 4.0 MHz |
| Transistors | 8,000 |
| Technology | CMOS |
| Package | 40-pin DIP |

## Architecture

- **Data Width:** 8-bit
- **CPI Range:** (2, 7)
- **Typical CPI:** 3.2

## Performance

- **IPS Range:** 800,000 - 1,500,000
- **MIPS (estimated):** 0.800 - 1.500
- **Typical CPI:** 3.2

## Performance Model

### Usage

```python
from wdc65c02_validated import WDC65C02Model

model = WDC65C02Model()
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
wdc65c02/
├── README.md                      # This documentation
├── current/
│   └── wdc65c02_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── wdc65c02_validation.json  # Validation data
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
