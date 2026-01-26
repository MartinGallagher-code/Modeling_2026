# Intel 4040 Performance Model

## Overview
Enhanced version of Intel 4004 with interrupts, more registers, and deeper stack.

## Directory Structure
```
intel_4040_models/
├── README.md
├── current/
│   └── intel_4040_validated.py
├── archive/
├── validation/
│   └── 4040_validated_model.json
└── docs/
```

## Key Specifications
| Parameter | Value |
|-----------|-------|
| Year | 1974 |
| Data Width | 4-bit |
| Clock | 740 kHz |
| Instructions | 60 (14 new) |
| Registers | 24 (vs 16) |
| Stack | 7-level (vs 3) |
| Interrupts | Yes |

## Performance
- **IPS**: 74,074 (typical)
- **kIPS**: 74.07
- **MIPS**: 0.074

## 4040 vs 4004
| Feature | 4004 | 4040 |
|---------|------|------|
| Instructions | 46 | 60 |
| Index Registers | 16 | 24 |
| Stack Depth | 3 | 7 |
| Interrupts | No | Yes |
| Timing | Same | Same |
