# Intel iAPX 432

## Overview

**Intel iAPX 432** (1981) - Failed capability-based architecture

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1981 |
| Manufacturer | Various |
| Data Width | 32-bit |
| Clock | 8.0 MHz |
| Transistors | 250,000 |
| Technology | NMOS |
| Package | Multi-chip |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (6, 400)
- **Typical CPI:** 50.0

## Performance

- **IPS Range:** 100,000 - 300,000
- **MIPS (estimated):** 0.100 - 0.300
- **Typical CPI:** 50.0

## Performance Model

### Usage

```python
from iapx432_validated import IAPX432Model

model = IAPX432Model()
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
iapx432/
├── README.md                      # This documentation
├── current/
│   └── iapx432_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── iapx432_validation.json  # Validation data
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
