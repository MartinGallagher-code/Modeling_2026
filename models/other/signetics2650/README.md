# Signetics 2650

## Overview

**Signetics 2650** (1975) - Early 8-bit with unique architecture

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1975 |
| Manufacturer | Various |
| Data Width | 8-bit |
| Clock | 1.25 MHz |
| Transistors | 5,000 |
| Technology | NMOS |
| Package | 40-pin DIP |

## Architecture

- **Data Width:** 8-bit
- **CPI Range:** (2, 5)
- **Typical CPI:** 3.0

## Performance

- **IPS Range:** 300,000 - 600,000
- **MIPS (estimated):** 0.300 - 0.600
- **Typical CPI:** 3.0

## Performance Model

### Usage

```python
from signetics2650_validated import SIGNETICS2650Model

model = SIGNETICS2650Model()
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
signetics2650/
├── README.md                      # This documentation
├── current/
│   └── signetics2650_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── signetics2650_validation.json  # Validation data
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
