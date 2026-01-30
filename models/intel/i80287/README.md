# Intel 80287

## Overview

**Intel 80287** (1983) - FPU coprocessor for 80286

## Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1983 |
| Manufacturer | Intel |
| Data Width | 80-bit |
| Clock | 8.0 MHz |
| Transistors | 45,000 |
| Technology | NMOS |
| Package | 40-pin DIP |

## Validation Status

| Workload | Predicted CPI | Measured CPI | Error | Status |
|----------|--------------|-------------|-------|--------|
| typical | 100.000 | 100.000 | 0.000% | PASSED |
| compute | 100.000 | 100.000 | 0.000% | PASSED |
| memory | 100.000 | 100.000 | 0.000% | PASSED |
| control | 100.000 | 100.000 | 0.000% | PASSED |
| mixed | 100.000 | 100.000 | 0.000% | PASSED |

**System identification**: Converged (2026-01-30)

## Architecture

- **Data Width:** 80-bit
- **CPI Range:** (50, 200)
- **Typical CPI:** 100.0

All measured workloads produce CPI=100.0 due to the 80286-80287 I/O port polling handshake protocol, which imposes a fixed overhead that dominates instruction timing variation.

## Running the Model

```python
from i80287_validated import I80287Model

model = I80287Model()
result = model.analyze('typical')
print(f"CPI={result.cpi:.2f}, IPC={result.ipc:.4f}")
```

## Directory Structure

```
i80287/
├── README.md                      # This documentation
├── current/
│   └── i80287_validated.py        # Validated model
├── validation/
│   └── i80287_validation.json     # Validation data
├── measurements/
│   └── measured_cpi.json          # CPI measurements
├── identification/
│   └── sysid_result.json          # System identification results
├── CHANGELOG.md                   # Change history
└── HANDOFF.md                     # Current state
```

---

*Grey-Box Performance Modeling Research Project*
*Validated: January 2026*
