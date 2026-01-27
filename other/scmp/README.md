# National SC/MP

## Overview

**National SC/MP** (1974) - Simple Cost-effective Micro Processor

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1974 |
| Manufacturer | Various |
| Data Width | 8-bit |
| Clock | 1.0 MHz |
| Transistors | 3,000 |
| Technology | PMOS |
| Package | 40-pin DIP |

## Architecture

- **Data Width:** 8-bit
- **CPI Range:** (5, 22)
- **Typical CPI:** 10.0

## Performance

- **IPS Range:** 50,000 - 150,000
- **MIPS (estimated):** 0.050 - 0.150
- **Typical CPI:** 10.0

## Performance Model

### Usage

```python
from scmp_validated import SCMPModel

model = SCMPModel()
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
scmp/
├── README.md                      # This documentation
├── current/
│   └── scmp_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── scmp_validation.json  # Validation data
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
