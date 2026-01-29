# ARM2

## Overview

ARM2 Grey-Box Queueing Model

## Directory Structure

```
arm2/
├── README.md                    # This file
├── current/
│   └── arm2_validated.py  # Current validated model
├── archive/                     # Previous model versions
├── validation/
│   └── arm2_validation.json  # Validation data
└── docs/                        # Additional documentation
```

## Usage

```python
from arm2_validated import ARM2Model

model = ARM2Model()
result = model.analyze('typical')

print(f"IPC: {result.ipc:.4f}")
print(f"CPI: {result.cpi:.2f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Migration Info

- **Migrated from**: `old/ARM2`
- **Migration date**: 2026-01-27
- **Family**: other

## Validation Status

⚠️ **MIGRATED** - Validation should be re-run after migration.

