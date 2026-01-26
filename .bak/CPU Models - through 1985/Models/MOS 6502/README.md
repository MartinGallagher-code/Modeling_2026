# MOS 6502 Performance Models

This directory contains performance models for the MOS 6502 processor family, organized with both current validated models and archived historical versions.

## Directory Structure

```
6502_models/
├── README.md                    # This file
├── current/                     # Active, validated models
│   └── mos_6502_validated.py    # Primary model (USE THIS)
├── archive/                     # Historical versions (deprecated)
│   └── mos_6502_cpi_stack_v1.py # Original simplified model
├── validation/                  # Validation data and sources
│   ├── 6502_validated_model.json
│   └── 6502_validation_data.md  # Research compilation
└── docs/                        # Documentation
    └── 6502_improvements_summary.md
```

## Quick Start

```python
# Use the validated model
from current.mos_6502_validated import MOS6502Model, WORKLOADS_6502

# Create model for a specific system
model = MOS6502Model("apple_ii")  # or "commodore_64", "nes", etc.

# Analyze performance
result = model.analyze("typical")

print(f"CPI: {result.cpi:.3f}")
print(f"IPC: {result.ipc:.4f}")
print(f"MIPS: {result.mips:.4f}")
print(f"Validation: {result.validation_status}")
```

## Model Comparison

| Model | CPI | IPC | MIPS @ 1MHz | Status |
|-------|-----|-----|-------------|--------|
| **mos_6502_validated.py** | 3.216 | 0.311 | 0.311 | ✓ Current |
| mos_6502_cpi_stack_v1.py | ~3.0 | ~0.33 | ~0.33 | Archived |

## Validated Model Features

The current validated model includes:

### Complete Instruction Database
- All 56 legal 6502 instructions
- Per-addressing-mode cycle counts
- Page boundary crossing penalties (+1 cycle)
- Branch timing: 2/3/4 cycles (not taken/taken/page cross)

### System Configurations
| System | Clock | Notes |
|--------|-------|-------|
| Generic 6502 | 1.000 MHz | Standard reference |
| Apple II | 1.023 MHz | NTSC timing |
| Apple II PAL | 1.018 MHz | PAL regions |
| Commodore 64 | 0.985 MHz | VIC-II cycle stealing |
| Atari 800 | 1.790 MHz | ANTIC DMA |
| NES/Famicom | 1.790 MHz | 2A03 variant |
| BBC Micro | 2.000 MHz | Acorn |

### Workload Profiles
- **typical**: General application code
- **compute**: Math-heavy (Sieve benchmark)
- **memory**: Block copy, table lookup
- **control**: State machines, menus
- **game**: Sprite handling, collision

## Validation Sources

1. **MCS6500 Family Hardware Manual** (MOS Technology, 1976)
2. **VICE Emulator** - Cycle-accurate verification
3. **Visual 6502** (visual6502.org) - Transistor-level simulation
4. **Klaus Dormann Test Suite** - Functional validation
5. **BYTE Magazine Sieve Benchmark** (1981-1983)

## Why Keep the Archive?

The archived model is retained for:
- **Version history**: Shows modeling evolution
- **Comparison baseline**: Demonstrates validation improvement
- **Educational reference**: Simpler model for learning
- **Fallback**: In case of edge cases

## Integration with Unified Interface

To use the validated model in the unified interface:

```python
from current.mos_6502_validated import get_improved_6502_config

# Get validated configuration
config = get_improved_6502_config()

# Update PROCESSORS dict
PROCESSORS["MOS 6502"].update(config)
```

## Running the Models

```bash
# Run validated model with full output
python current/mos_6502_validated.py

# Run archived model (shows deprecation warning)
python archive/mos_6502_cpi_stack_v1.py
```

## Files Description

| File | Purpose |
|------|---------|
| `current/mos_6502_validated.py` | Primary model - use this |
| `archive/mos_6502_cpi_stack_v1.py` | Original simplified model |
| `validation/6502_validated_model.json` | Exported validation data |
| `validation/6502_validation_data.md` | Research sources compilation |
| `docs/6502_improvements_summary.md` | Detailed change documentation |

---

**Model Version**: 2.0 (Validated)  
**Last Updated**: January 25, 2026  
**Validation Status**: PASS (19/19 instruction timing tests)
