# Intel 8086

## Overview

**Intel 8086** (1978) - Foundation of x86 architecture

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1978 |
| Manufacturer | Various |
| Data Width | 16-bit |
| Clock | 5.0 MHz |
| Transistors | 29,000 |
| Technology | 3µm NMOS |
| Package | 40-pin DIP |

## Architecture

- **Data Width:** 16-bit
- **CPI Range:** (2, 200)
- **Typical CPI:** 12.0

## Performance

- **IPS Range:** 330,000 - 750,000
- **MIPS (estimated):** 0.330 - 0.750
- **Typical CPI:** 12.0

## Performance Model

### Usage

```python
from i8086_validated import I8086Model

model = I8086Model()
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
i8086/
├── README.md                      # This documentation
├── current/
│   └── i8086_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── i8086_validation.json  # Validation data
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
