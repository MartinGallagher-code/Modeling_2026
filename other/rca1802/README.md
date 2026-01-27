# RCA 1802

## Overview

**RCA 1802** (1976) - First CMOS microprocessor, Voyager

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1976 |
| Manufacturer | Various |
| Data Width | 8-bit |
| Clock | 3.2 MHz |
| Transistors | 5,000 |
| Technology | CMOS |
| Package | 40-pin DIP |

## Architecture

- **Data Width:** 8-bit
- **CPI Range:** (8, 24)
- **Typical CPI:** 12.0

## Performance

- **IPS Range:** 100,000 - 300,000
- **MIPS (estimated):** 0.100 - 0.300
- **Typical CPI:** 12.0

## Performance Model

### Usage

```python
from rca1802_validated import RCA1802Model

model = RCA1802Model()
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
rca1802/
├── README.md                      # This documentation
├── current/
│   └── rca1802_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── rca1802_validation.json  # Validation data
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
