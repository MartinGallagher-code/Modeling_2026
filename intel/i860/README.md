# Intel i860

## Overview

Intel i860 Grey-Box Queueing Model

## Directory Structure

```
i860/
├── README.md                    # This file
├── current/
│   └── i860_validated.py  # Current validated model
├── archive/                     # Previous model versions
├── validation/
│   └── i860_validation.json  # Validation data
└── docs/                        # Additional documentation
```

## Usage

```python
from i860_validated import I860Model

model = I860Model()
result = model.analyze('typical')

print(f"IPC: {result.ipc:.4f}")
print(f"CPI: {result.cpi:.2f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Migration Info

- **Migrated from**: `old/Intel i860`
- **Migration date**: 2026-01-27
- **Family**: intel

## Validation Status

✅ **VALIDATED** - CPI error: 4.8% (target: <5%)

