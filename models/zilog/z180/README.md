# Zilog Z180

## Overview

**Zilog Z180** (1985) - Enhanced Z80 with MMU

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1985 |
| Manufacturer | Various |
| Data Width | 8-bit |
| Clock | 6.0 MHz |
| Transistors | 20,000 |
| Technology | CMOS |
| Package | 64-pin DIP |

## Architecture

- **Data Width:** 8-bit
- **CPI Range:** (3, 20)
- **Typical CPI:** 5.5

## Performance

- **IPS Range:** 800,000 - 1,800,000
- **MIPS (estimated):** 0.800 - 1.800
- **Typical CPI:** 5.5

## Performance Model

### Usage

```python
from z180_validated import Z180Model

model = Z180Model()
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
z180/
├── README.md                      # This documentation
├── current/
│   └── z180_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── z180_validation.json  # Validation data
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
