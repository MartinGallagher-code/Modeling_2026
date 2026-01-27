# Zilog Z80000

## Overview

**Zilog Z80000** (1986) - Zilog's 32-bit processor

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1986 |
| Manufacturer | Various |
| Data Width | 32-bit |
| Clock | 16.0 MHz |
| Transistors | 91,000 |
| Technology | CMOS |
| Package | 132-pin PGA |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (3, 80)
- **Typical CPI:** 6.0

## Performance

- **IPS Range:** 2,000,000 - 4,500,000
- **MIPS (estimated):** 2.000 - 4.500
- **Typical CPI:** 6.0

## Performance Model

### Usage

```python
from z80000_validated import Z80000Model

model = Z80000Model()
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
z80000/
├── README.md                      # This documentation
├── current/
│   └── z80000_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── z80000_validation.json  # Validation data
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
