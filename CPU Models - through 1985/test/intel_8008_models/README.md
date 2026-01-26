# Intel 8008 Performance Model

## Overview
First 8-bit microprocessor (April 1972). Architecture designed by CTC (Datapoint 2200).

## Directory Structure
```
intel_8008_models/
├── README.md
├── current/
│   └── intel_8008_validated.py
├── archive/
├── validation/
│   └── 8008_validated_model.json
└── docs/
```

## Key Specifications
| Parameter | Value |
|-----------|-------|
| Year | 1972 |
| Data Width | 8-bit |
| Address Space | 16 KB (14-bit) |
| Clock | 500-800 kHz |
| T-state | 2 clock cycles |

## IMPORTANT: Timing
Unlike the 8080, each T-state = 2 clock cycles!
- Instructions: 5-11 T-states = 10-22 clock cycles

## Performance (8008 @ 500 kHz)
- **IPS**: 33,333 (typical)
- **MIPS**: 0.033

Note: The 8008 is ~10× slower than 6502 @ 1 MHz
