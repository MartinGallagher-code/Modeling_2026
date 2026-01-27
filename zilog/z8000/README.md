# Zilog Z8000

## Overview

**Zilog Z8000** (1979) - Zilog's 16-bit processor

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1979 |
| Manufacturer | Various |
| Data Width | 16-bit |
| Clock | 4.0 MHz |
| Transistors | 17,500 |
| Technology | NMOS |
| Package | 48-pin DIP |

## Architecture

- **Data Width:** 16-bit
- **CPI Range:** (3, 100)
- **Typical CPI:** 8.0

## Performance

- **IPS Range:** 350,000 - 800,000
- **MIPS (estimated):** 0.350 - 0.800
- **Typical CPI:** 8.0

## Performance Model

### Usage

```python
from z8000_validated import Z8000Model

model = Z8000Model()
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
z8000/
├── README.md                      # This documentation
├── current/
│   └── z8000_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── z8000_validation.json  # Validation data
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
