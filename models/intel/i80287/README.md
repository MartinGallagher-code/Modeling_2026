# Intel 80287

## Overview

**Intel 80287** (1983) - FPU coprocessor for 80286

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1983 |
| Manufacturer | Various |
| Data Width | 80-bit |
| Clock | 8.0 MHz |
| Transistors | 45,000 |
| Technology | NMOS |
| Package | 40-pin DIP |

## Architecture

- **Data Width:** 80-bit
- **CPI Range:** (50, 200)
- **Typical CPI:** 100.0

## Performance

- **IPS Range:** 50,000 - 150,000
- **MIPS (estimated):** 0.050 - 0.150
- **Typical CPI:** 100.0

## Performance Model

### Usage

```python
from i80287_validated import I80287Model

model = I80287Model()
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
i80287/
├── README.md                      # This documentation
├── current/
│   └── i80287_validated.py     # ✓ Validated model (USE THIS)
├── archive/                       # Deprecated versions
├── validation/
│   └── i80287_validation.json  # Validation data
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
