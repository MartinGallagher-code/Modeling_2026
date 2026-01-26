# Intel 80188 Performance Model

## Overview
Same as 80186 but with 8-bit external data bus for lower cost systems.

## Directory Structure
```
intel_80188_models/
├── README.md
├── current/
│   └── intel_80188_validated.py
├── archive/
├── validation/
│   └── 80188_validated_model.json
└── docs/
```

## Key Specifications
| Parameter | Value |
|-----------|-------|
| Year | 1982 |
| Internal Width | 16-bit |
| External Bus | 8-bit |
| Clock | 6-25 MHz |

## 80188 vs 80186
| Feature | 80186 | 80188 |
|---------|-------|-------|
| External bus | 16-bit | 8-bit |
| Word transfer | 1 cycle | 2 cycles |
| Performance | 1.0× | 0.7-0.9× |
| Cost | Higher | Lower |

## Performance (@ 8 MHz)
- **MIPS**: 0.91
- ~30-40% slower than 80186 for memory-heavy code
