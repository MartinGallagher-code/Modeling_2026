# AIM  PPC 601

## Overview

AIM  PPC 601 Grey-Box Queueing Model

## Directory Structure

```
aim__ppc_601/
├── README.md                    # This file
├── current/
│   └── aim__ppc_601_validated.py  # Current validated model
├── archive/                     # Previous model versions
├── validation/
│   └── aim__ppc_601_validation.json  # Validation data
└── docs/                        # Additional documentation
```

## Usage

```python
from aim__ppc_601_validated import AIMPPC601Model

model = AIMPPC601Model()
result = model.analyze('typical')

print(f"IPC: {result.ipc:.4f}")
print(f"CPI: {result.cpi:.2f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Migration Info

- **Migrated from**: `old/AIM  PPC 601`
- **Migration date**: 2026-01-27
- **Family**: other

## Validation Status

⚠️ **MIGRATED** - Validation should be re-run after migration.

