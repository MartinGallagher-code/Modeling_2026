# Intel 80386

## Overview

**Intel 80386** (1985) - First x86 32-bit processor

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1985 |
| Manufacturer | Various |
| Data Width | 32-bit |
| Clock | 16.0 MHz |
| Transistors | 275,000 |
| Technology | 1.5µm CMOS |
| Package | 132-pin PGA |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (2, 40)
- **Typical CPI:** 4.4

## Performance

- **IPS Range:** 3,000,000 - 6,000,000
- **MIPS (estimated):** 3.000 - 6.000
- **Typical CPI:** 4.4

## Performance Model

### Usage

```python
from i80386_validated import I80386Model

model = I80386Model()
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
i80386/
├── README.md                      # This documentation
├── current/
│   └── i80386_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── i80386_validation.json  # Validation data
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
