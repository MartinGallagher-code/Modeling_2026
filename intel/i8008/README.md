# Intel 8008

## Overview

**Intel 8008** (1972) - First 8-bit microprocessor

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1972 |
| Manufacturer | Various |
| Data Width | 8-bit |
| Clock | 0.5 MHz |
| Transistors | 3,500 |
| Technology | 10µm PMOS |
| Package | 18-pin DIP |

## Architecture

- **Data Width:** 8-bit
- **CPI Range:** (1, 3)
- **Typical CPI:** 2.0

## Performance

- **IPS Range:** 30,000 - 80,000
- **MIPS (estimated):** 0.030 - 0.080
- **Typical CPI:** 2.0

## Performance Model

### Usage

```python
from i8008_validated import I8008Model

model = I8008Model()
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
i8008/
├── README.md                      # This documentation
├── current/
│   └── i8008_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── i8008_validation.json  # Validation data
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
