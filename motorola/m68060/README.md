# Motorola 68060

## Overview

Motorola 68060 Grey-Box Queueing Model

## Directory Structure

```
m68060/
├── README.md                    # This file
├── current/
│   └── m68060_validated.py  # Current validated model
├── archive/                     # Previous model versions
├── validation/
│   └── m68060_validation.json  # Validation data
└── docs/                        # Additional documentation
```

## Usage

```python
from m68060_validated import M68060Model

model = M68060Model()
result = model.analyze('typical')

print(f"IPC: {result.ipc:.4f}")
print(f"CPI: {result.cpi:.2f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Migration Info

- **Migrated from**: `old/Motorola 68060`
- **Migration date**: 2026-01-27
- **Family**: motorola

## Validation Status

⚠️ **MIGRATED** - Validation should be re-run after migration.

