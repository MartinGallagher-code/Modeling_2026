# Documentation

## Overview

Documentation Grey-Box Queueing Model

## Directory Structure

```
documentation/
├── README.md                    # This file
├── current/
│   └── documentation_validated.py  # Current validated model
├── archive/                     # Previous model versions
├── validation/
│   └── documentation_validation.json  # Validation data
└── docs/                        # Additional documentation
```

## Usage

```python
from documentation_validated import DOCUMENTATIONModel

model = DOCUMENTATIONModel()
result = model.analyze('typical')

print(f"IPC: {result.ipc:.4f}")
print(f"CPI: {result.cpi:.2f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Migration Info

- **Migrated from**: `old/Documentation`
- **Migration date**: 2026-01-27
- **Family**: other

## Validation Status

⚠️ **MIGRATED** - Validation should be re-run after migration.

