# Intel 4040

## Overview

**Intel 4040** (1974) - Enhanced 4004 with interrupts

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1974 |
| Manufacturer | Various |
| Data Width | 4-bit |
| Clock | 0.74 MHz |
| Transistors | 3,000 |
| Technology | 10µm PMOS |
| Package | 24-pin DIP |

## Architecture

- **Data Width:** 4-bit
- **CPI Range:** (1, 2)
- **Typical CPI:** 1.5

## Performance

- **IPS Range:** 50,000 - 92,500
- **MIPS (estimated):** 0.050 - 0.092
- **Typical CPI:** 1.5

## Performance Model

### Usage

```python
from i4040_validated import I4040Model

model = I4040Model()
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
i4040/
├── README.md                      # This documentation
├── current/
│   └── i4040_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── i4040_validation.json  # Validation data
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
