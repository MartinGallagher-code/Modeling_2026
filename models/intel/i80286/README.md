# Intel 80286

## Overview

**Intel 80286** (1982) - Protected mode, IBM PC/AT CPU

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1982 |
| Manufacturer | Various |
| Data Width | 16-bit |
| Clock | 8.0 MHz |
| Transistors | 134,000 |
| Technology | 1.5µm CMOS |
| Package | 68-pin LCC |

## Architecture

- **Data Width:** 16-bit
- **CPI Range:** (2, 25)
- **Typical CPI:** 4.8

## Performance

- **IPS Range:** 1,500,000 - 2,500,000
- **MIPS (estimated):** 1.500 - 2.500
- **Typical CPI:** 4.8

## Performance Model

### Usage

```python
from i80286_validated import I80286Model

model = I80286Model()
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
i80286/
├── README.md                      # This documentation
├── current/
│   └── i80286_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── i80286_validation.json  # Validation data
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
