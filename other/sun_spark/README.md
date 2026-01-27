# Sun SPARK

## Overview

Sun SPARK Grey-Box Queueing Model

## Directory Structure

```
sun_spark/
├── README.md                    # This file
├── current/
│   └── sun_spark_validated.py  # Current validated model
├── archive/                     # Previous model versions
├── validation/
│   └── sun_spark_validation.json  # Validation data
└── docs/                        # Additional documentation
```

## Usage

```python
from sun_spark_validated import SUNSPARKModel

model = SUNSPARKModel()
result = model.analyze('typical')

print(f"IPC: {result.ipc:.4f}")
print(f"CPI: {result.cpi:.2f}")
print(f"Bottleneck: {result.bottleneck}")
```

## Migration Info

- **Migrated from**: `old/Sun SPARK`
- **Migration date**: 2026-01-27
- **Family**: other

## Validation Status

⚠️ **MIGRATED** - Validation should be re-run after migration.

