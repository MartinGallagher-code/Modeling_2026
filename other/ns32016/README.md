# NS32016

## Overview

**NS32016** (1982) - National Semi 32-bit

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1982 |
| Manufacturer | Various |
| Data Width | 32-bit |
| Clock | 6.0 MHz |
| Transistors | 60,000 |
| Technology | NMOS |
| Package | 48-pin DIP |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (3, 100)
- **Typical CPI:** 12.0

## Performance

- **IPS Range:** 400,000 - 900,000
- **MIPS (estimated):** 0.400 - 0.900
- **Typical CPI:** 12.0

## Performance Model

### Usage

```python
from ns32016_validated import NS32016Model

model = NS32016Model()
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
ns32016/
├── README.md                      # This documentation
├── current/
│   └── ns32016_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── ns32016_validation.json  # Validation data
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
