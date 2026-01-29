# Zilog Z80A

## Overview

**Zilog Z80A** (1978) - Higher speed Z80

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1978 |
| Manufacturer | Various |
| Data Width | 8-bit |
| Clock | 4.0 MHz |
| Transistors | 8,500 |
| Technology | NMOS |
| Package | 40-pin DIP |

## Architecture

- **Data Width:** 8-bit
- **CPI Range:** (4, 23)
- **Typical CPI:** 7.8

## Performance

- **IPS Range:** 400,000 - 950,000
- **MIPS (estimated):** 0.400 - 0.950
- **Typical CPI:** 7.8

## Performance Model

### Usage

```python
from z80a_validated import Z80AModel

model = Z80AModel()
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
z80a/
├── README.md                      # This documentation
├── current/
│   └── z80a_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── z80a_validation.json  # Validation data
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
