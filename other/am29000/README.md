# AMD Am29000

## Overview

**AMD Am29000** (1988) - Early RISC processor

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1988 |
| Manufacturer | Various |
| Data Width | 32-bit |
| Clock | 25.0 MHz |
| Transistors | 450,000 |
| Technology | 1µm CMOS |
| Package | 169-pin PGA |

## Architecture

- **Data Width:** 32-bit
- **CPI Range:** (1, 4)
- **Typical CPI:** 1.5

## Performance

- **IPS Range:** 15,000,000 - 25,000,000
- **MIPS (estimated):** 15.000 - 25.000
- **Typical CPI:** 1.5

## Performance Model

### Usage

```python
from am29000_validated import AM29000Model

model = AM29000Model()
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
am29000/
├── README.md                      # This documentation
├── current/
│   └── am29000_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── am29000_validation.json  # Validation data
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
