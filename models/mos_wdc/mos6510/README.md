# MOS 6510

## Overview

**MOS 6510** (1982) - Commodore 64 CPU (6502 variant)

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1982 |
| Manufacturer | Various |
| Data Width | 8-bit |
| Clock | 1.0 MHz |
| Transistors | 3,510 |
| Technology | NMOS |
| Package | 40-pin DIP |

## Architecture

- **Data Width:** 8-bit
- **CPI Range:** (2, 7)
- **Typical CPI:** 3.5

## Performance

- **IPS Range:** 250,000 - 500,000
- **MIPS (estimated):** 0.250 - 0.500
- **Typical CPI:** 3.5

## Performance Model

### Usage

```python
from mos6510_validated import MOS6510Model

model = MOS6510Model()
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
mos6510/
├── README.md                      # This documentation
├── current/
│   └── mos6510_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── mos6510_validation.json  # Validation data
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
