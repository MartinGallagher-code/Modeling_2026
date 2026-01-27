# Models

## Overview

Models Grey-Box Queueing Model

## Directory Structure

```
models/
├── README.md                    # This file
├── current/
│   └── models_validated.py  # Current validated model
├── archive/                     # Previous model versions
├── validation/
│   └── models_validation.json  # Validation data
└── docs/                        # Additional documentation
```

## Usage

```python
from models_validated import MODELSModel

model = MODELSModel()
result = model.analyze('typical')

print(f"IPC: {result.ipc:.4f}")
print(f"CPI: {result.cpi:.2f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Migration Info

- **Migrated from**: `old/Models`
- **Migration date**: 2026-01-27
- **Family**: other

## Validation Status

⚠️ **MIGRATED** - Validation should be re-run after migration.

