# ARM6

## Overview

ARM6 Grey-Box Queueing Model

## Directory Structure

```
arm6/
├── README.md                    # This file
├── current/
│   └── arm6_validated.py  # Current validated model
├── archive/                     # Previous model versions
├── validation/
│   └── arm6_validation.json  # Validation data
└── docs/                        # Additional documentation
```

## Usage

```python
from arm6_validated import ARM6Model

model = ARM6Model()
result = model.analyze('typical')

print(f"IPC: {result.ipc:.4f}")
print(f"CPI: {result.cpi:.2f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Migration Info

- **Migrated from**: `old/ARM6`
- **Migration date**: 2026-01-27
- **Family**: other

## Validation Status

⚠️ **MIGRATED** - Validation should be re-run after migration.

