# Intel Pentium

## Overview

Intel Pentium Grey-Box Queueing Model

## Directory Structure

```
pentium/
├── README.md                    # This file
├── current/
│   └── pentium_validated.py  # Current validated model
├── archive/                     # Previous model versions
├── validation/
│   └── pentium_validation.json  # Validation data
└── docs/                        # Additional documentation
```

## Usage

```python
from pentium_validated import PENTIUMModel

model = PENTIUMModel()
result = model.analyze('typical')

print(f"IPC: {result.ipc:.4f}")
print(f"CPI: {result.cpi:.2f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Migration Info

- **Migrated from**: `old/Intel Pentium`
- **Migration date**: 2026-01-27
- **Family**: intel

## Validation Status

⚠️ **MIGRATED** - Validation should be re-run after migration.

