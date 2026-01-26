# Intel 80186 Performance Model

## Overview
Enhanced 8086 with integrated peripherals and faster execution.

## Directory Structure
```
intel_80186_models/
├── README.md
├── current/
│   └── intel_80186_validated.py
├── archive/
├── validation/
│   └── 80186_validated_model.json
└── docs/
```

## Key Specifications
| Parameter | Value |
|-----------|-------|
| Year | 1982 |
| Data Width | 16-bit |
| External Bus | 16-bit |
| Clock | 6-25 MHz |
| Transistors | 55,000 |

## Integrated Peripherals
- Clock generator
- 2 DMA channels
- Interrupt controller
- 3 16-bit timers

## Timing Improvements vs 8086
| Operation | 8086 | 80186 | Speedup |
|-----------|------|-------|---------|
| MUL 16-bit | 118-133 | 26-28 | ~4.5× |
| DIV 16-bit | 144-162 | 29 | ~5× |
| Shifts | 8+4n | 5+n | ~4× |

## Performance (@ 8 MHz)
- **MIPS**: 1.02
- **Speedup vs 8086**: 1.53×
