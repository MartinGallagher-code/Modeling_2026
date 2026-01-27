# DEC Alpha 21064

## Overview

DEC Alpha 21064 Grey-Box Queueing Model

## Directory Structure

```
alpha21064/
├── README.md                    # This file
├── current/
│   └── alpha21064_validated.py  # Current validated model
├── archive/                     # Previous model versions
├── validation/
│   └── alpha21064_validation.json  # Validation data
└── docs/                        # Additional documentation
```

## Usage

```python
from alpha21064_validated import ALPHA21064Model

model = ALPHA21064Model()
result = model.analyze('typical')

print(f"IPC: {result.ipc:.4f}")
print(f"CPI: {result.cpi:.2f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Migration Info

- **Migrated from**: `old/DEC Alpha 21064`
- **Migration date**: 2026-01-27
- **Family**: other

## Validation Status

⚠️ **MIGRATED** - Validation should be re-run after migration.

