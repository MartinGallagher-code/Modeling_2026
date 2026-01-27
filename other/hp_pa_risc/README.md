# HP pa RISC

## Overview

HP pa RISC Grey-Box Queueing Model

## Directory Structure

```
hp_pa_risc/
├── README.md                    # This file
├── current/
│   └── hp_pa_risc_validated.py  # Current validated model
├── archive/                     # Previous model versions
├── validation/
│   └── hp_pa_risc_validation.json  # Validation data
└── docs/                        # Additional documentation
```

## Usage

```python
from hp_pa_risc_validated import HPPARISCModel

model = HPPARISCModel()
result = model.analyze('typical')

print(f"IPC: {result.ipc:.4f}")
print(f"CPI: {result.cpi:.2f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Migration Info

- **Migrated from**: `old/HP pa RISC`
- **Migration date**: 2026-01-27
- **Family**: other

## Validation Status

⚠️ **MIGRATED** - Validation should be re-run after migration.

