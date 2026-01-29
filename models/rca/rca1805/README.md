# RCA 1805

## Overview

**RCA 1805** (1978) - Enhanced 1802

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1978 |
| Manufacturer | Various |
| Data Width | 8-bit |
| Clock | 4.0 MHz |
| Transistors | 6,000 |
| Technology | CMOS |
| Package | 40-pin DIP |

## Architecture

- **Data Width:** 8-bit
- **CPI Range:** (8, 24)
- **Typical CPI:** 10.0

## Performance

- **IPS Range:** 150,000 - 400,000
- **MIPS (estimated):** 0.150 - 0.400
- **Typical CPI:** 10.0

## Performance Model

### Usage

```python
from rca1805_validated import RCA1805Model

model = RCA1805Model()
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
rca1805/
├── README.md                      # This documentation
├── current/
│   └── rca1805_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── rca1805_validation.json  # Validation data
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
