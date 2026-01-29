# TI SN74181

## Overview

**TI SN74181** (1970) - First single-chip 4-bit ALU

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1970 |
| Manufacturer | Texas Instruments |
| Data Width | 4-bit |
| Clock Equivalent | 45.0 MHz (1/22ns) |
| Transistors | 75 |
| Technology | TTL |
| Package | 24-pin DIP |

## Architecture

- **Type:** Combinational ALU (NOT a CPU)
- **Functions:** 16 arithmetic + 16 logic = 32 total
- **CPI:** 1.0 (all operations single propagation delay)
- **Propagation Delay:** ~22ns typical

## Performance

- **Operations/sec:** ~45,000,000 (at propagation delay limit)
- **Typical CPI:** 1.0

## Performance Model

### Usage

```python
from sn74181_validated import SN74181Model

model = SN74181Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"Bottleneck: {result.bottleneck}")

# Validate against known specifications
validation = model.validate()
for test in validation['tests']:
    status = "PASS" if test['passed'] else "FAIL"
    print(f"{test['name']}: {status}")
```

## Directory Structure

```
sn74181/
├── README.md                        # This documentation
├── HANDOFF.md                       # Handoff notes
├── CHANGELOG.md                     # Change history
├── __init__.py                      # Module init
├── current/
│   └── sn74181_validated.py         # Validated model (USE THIS)
└── validation/
    └── sn74181_validation.json      # Validation data
```

## Validation

| Test | Status |
|------|--------|
| CPI Accuracy | Validated (1.0, 0% error) |
| Weight Sums | All workloads sum to 1.0 |
| Cycle Ranges | All within expected bounds |

**Target Accuracy:** +/-5% for performance estimates

---

*Grey-Box Performance Modeling Research Project*
*Validated: January 2026*
