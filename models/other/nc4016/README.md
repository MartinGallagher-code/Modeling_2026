# Novix NC4016

## Overview

**Novix NC4016** (1985) - Forth stack machine

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1985 |
| Manufacturer | Various |
| Data Width | 16-bit |
| Clock | 8.0 MHz |
| Transistors | 4,000 |
| Technology | CMOS |
| Package | 68-pin PLCC |

## Architecture

- **Data Width:** 16-bit
- **CPI Range:** (1, 3)
- **Typical CPI:** 1.2

## Performance

- **IPS Range:** 5,000,000 - 8,000,000
- **MIPS (estimated):** 5.000 - 8.000
- **Typical CPI:** 1.2

## Performance Model

### Usage

```python
from nc4016_validated import NC4016Model

model = NC4016Model()
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
nc4016/
├── README.md                      # This documentation
├── current/
│   └── nc4016_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── nc4016_validation.json  # Validation data
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
