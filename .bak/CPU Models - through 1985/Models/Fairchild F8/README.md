# Fairchild F8 (3850) Performance Model

## Overview
Multi-chip 8-bit microcontroller family. Used in Fairchild Channel F game console.

## Directory Structure
```
fairchild_f8_models/
├── README.md
├── current/
│   └── fairchild_f8_validated.py
├── archive/
├── validation/
│   └── f8_validated_model.json
└── docs/
```

## Key Specifications
| Parameter | Value |
|-----------|-------|
| Year | 1975 |
| Data Width | 8-bit |
| Clock | 1-2 MHz |
| Cycle Time | 2 µs @ 2 MHz |
| Scratchpad | 64 bytes |

## Timing
- Short cycle: 4 φ periods
- Long cycle: 6 φ periods

## Performance (F3850 @ 2 MHz)
- **IPS**: 408,163
- **MIPS**: 0.41

## Usage
```python
from fairchild_f8_validated import FairchildF8Model
model = FairchildF8Model("f3850_2mhz")
result = model.analyze("typical")
```
