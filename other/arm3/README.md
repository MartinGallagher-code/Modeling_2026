# ARM3

## Overview

ARM3 Grey-Box Queueing Model

## Directory Structure

```
arm3/
├── README.md                    # This file
├── current/
│   └── arm3_validated.py  # Current validated model
├── archive/                     # Previous model versions
├── validation/
│   └── arm3_validation.json  # Validation data
└── docs/                        # Additional documentation
```

## Usage

```python
from arm3_validated import ARM3Model

model = ARM3Model()
result = model.analyze('typical')

print(f"IPC: {result.ipc:.4f}")
print(f"CPI: {result.cpi:.2f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Migration Info

- **Migrated from**: `old/ARM3`
- **Migration date**: 2026-01-27
- **Family**: other

## Validation Status

⚠️ **MIGRATED** - Validation should be re-run after migration.

