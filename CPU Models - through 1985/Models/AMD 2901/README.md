# AMD 2901 Bit-Slice Performance Model

## Overview
The AMD 2901 is a 4-bit bit-slice ALU, not a standalone processor. Multiple 2901s are cascaded to create wider data paths (8, 16, 32-bit systems).

## Directory Structure
```
amd_2901_models/
├── README.md
├── current/
│   └── amd_2901_validated.py    # Validated model
├── archive/                      # Original models
├── validation/
│   └── 2901_validated_model.json
└── docs/
```

## Key Specifications
| Parameter | Value |
|-----------|-------|
| Year | 1975 |
| Type | 4-bit bit-slice |
| Clock | 20-40 MHz |
| Technology | Bipolar |
| Register File | 16 × 4-bit |

## Performance (16-bit system @ 20 MHz)
- **MIPS**: 5.71 (macro-instructions)
- **Speedup vs 8085**: 15.4×

## Usage
```python
from amd_2901_validated import AMD2901Model
model = AMD2901Model(clock_mhz=20.0, slices=4)  # 16-bit system
result = model.analyze("typical")
print(f"MIPS: {result.mips:.2f}")
```
