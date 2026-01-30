# NEC uPD7725 Processor Model

## Overview
- **Manufacturer**: NEC
- **Year**: 1985
- **Architecture**: 16-bit Enhanced DSP
- **Technology**: CMOS
- **Clock**: 8 MHz
- **Transistors**: ~30,000
- **Target CPI**: 1.5
- **Usage**: DSP coprocessor (SNES DSP-1, audio, communications)

## Model Description
Grey-box queueing model for the NEC uPD7725, an enhanced digital signal processor. Best known as the DSP-1 coprocessor in SNES cartridges, it performed coordinate transformations and other math-heavy operations with single-cycle MAC capability.

## Instruction Categories
| Category      | Cycles | Description |
|--------------|--------|-------------|
| mac           | 1      | Single-cycle multiply-accumulate |
| alu           | 1      | ALU operations |
| data_transfer | 2      | Data transfer operations |
| control       | 2      | Branch, jump, loop |
| memory        | 3      | External memory access |

## Validation Status
- **Status**: PASSED
- **CPI Error**: 0.00%
- **Last Validated**: 2026-01-29

## Files
- `current/upd7725_validated.py` - Validated processor model
- `validation/upd7725_validation.json` - Validation data and timing references
