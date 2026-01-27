# Intel 80186

## Overview

**Intel 80186** (1982) - Embedded 8086 with peripherals

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1982 |
| Manufacturer | Various |
| Data Width | 16-bit |
| Clock | 8.0 MHz |
| Transistors | 55,000 |
| Technology | NMOS |
| Package | 68-pin LCC |

## Architecture

- **Data Width:** 16-bit
- **CPI Range:** (2, 40)
- **Typical CPI:** 8.0

## Performance

- **IPS Range:** 800,000 - 1,500,000
- **MIPS (estimated):** 0.800 - 1.500
- **Typical CPI:** 8.0

## Performance Model

### Usage

```python
from i80186_validated import I80186Model

model = I80186Model()
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
i80186/
├── README.md                      # This documentation
├── current/
│   └── i80186_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── i80186_validation.json  # Validation data
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
