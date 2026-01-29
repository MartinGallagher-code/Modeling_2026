# Zilog Z80B

## Overview

**Zilog Z80B** (1980) - 6 MHz Z80

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1980 |
| Manufacturer | Various |
| Data Width | 8-bit |
| Clock | 6.0 MHz |
| Transistors | 8,500 |
| Technology | NMOS |
| Package | 40-pin DIP |

## Architecture

- **Data Width:** 8-bit
- **CPI Range:** (4, 23)
- **Typical CPI:** 7.8

## Performance

- **IPS Range:** 600,000 - 1,400,000
- **MIPS (estimated):** 0.600 - 1.400
- **Typical CPI:** 7.8

## Performance Model

### Usage

```python
from z80b_validated import Z80BModel

model = Z80BModel()
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
z80b/
├── README.md                      # This documentation
├── current/
│   └── z80b_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── z80b_validation.json  # Validation data
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
