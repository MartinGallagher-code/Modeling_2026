# Intel 80387

## Overview

**Intel 80387** (1987) - FPU coprocessor for 80386

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1987 |
| Manufacturer | Various |
| Data Width | 80-bit |
| Clock | 16.0 MHz |
| Transistors | 104,000 |
| Technology | CMOS |
| Package | 68-pin PGA |

## Architecture

- **Data Width:** 80-bit
- **CPI Range:** (20, 140)
- **Typical CPI:** 50.0

## Performance

- **IPS Range:** 200,000 - 800,000
- **MIPS (estimated):** 0.200 - 0.800
- **Typical CPI:** 50.0

## Performance Model

### Usage

```python
from i80387_validated import I80387Model

model = I80387Model()
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
i80387/
├── README.md                      # This documentation
├── current/
│   └── i80387_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── i80387_validation.json  # Validation data
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
