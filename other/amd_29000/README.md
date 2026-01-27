# AMD 29000

## Overview

AMD 29000 Grey-Box Queueing Model

## Directory Structure

```
amd_29000/
├── README.md                    # This file
├── current/
│   └── amd_29000_validated.py  # Current validated model
├── archive/                     # Previous model versions
├── validation/
│   └── amd_29000_validation.json  # Validation data
└── docs/                        # Additional documentation
```

## Usage

```python
from amd_29000_validated import AMD29000Model

model = AMD29000Model()
result = model.analyze('typical')

print(f"IPC: {result.ipc:.4f}")
print(f"CPI: {result.cpi:.2f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Migration Info

- **Migrated from**: `old/AMD 29000`
- **Migration date**: 2026-01-27
- **Family**: other

## Validation Status

⚠️ **MIGRATED** - Validation should be re-run after migration.

