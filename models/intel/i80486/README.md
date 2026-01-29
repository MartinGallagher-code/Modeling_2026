# Intel 80486

## Overview

Intel 80486 Grey-Box Queueing Model

## Directory Structure

```
i80486/
├── README.md                    # This file
├── current/
│   └── i80486_validated.py  # Current validated model
├── archive/                     # Previous model versions
├── validation/
│   └── i80486_validation.json  # Validation data
└── docs/                        # Additional documentation
```

## Usage

```python
from i80486_validated import I80486Model

model = I80486Model()
result = model.analyze('typical')

print(f"IPC: {result.ipc:.4f}")
print(f"CPI: {result.cpi:.2f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Migration Info

- **Migrated from**: `old/Intel 80486`
- **Migration date**: 2026-01-27
- **Family**: intel

## Validation Status

⚠️ **MIGRATED** - Validation should be re-run after migration.

