# AMD Am29C101 Processor Model

## Overview
- **Manufacturer**: AMD
- **Year**: 1982
- **Architecture**: 16-bit Integrated CMOS Bit-Slice
- **Technology**: CMOS
- **Transistors**: ~20000
- **Clock**: 20 MHz
- **Target CPI**: 2.5

## Model Description
Grey-box queueing model for the AMD Am29C101. This chip integrated four Am2901 4-bit ALU slices into a single CMOS chip, providing a complete 16-bit datapath with lower power consumption than the original bipolar Am2901 design.

## Instruction Categories
| Category | Cycles | Description |
|----------|--------|-------------|
| alu      | 2.0    | 16-bit ALU operations |
| shift    | 2.5    | Shift and rotate |
| logic    | 2.0    | Logic operations |
| control  | 3.0    | Microsequencer control |
| cascade  | 3.0    | Internal slice cascade |

## Validation Status
- **Status**: PASSED
- **CPI Error**: 0.0%
- **Last Validated**: 2026-01-29

## Files
- `current/am29c101_validated.py` - Validated processor model
- `validation/am29c101_validation.json` - Validation data and timing references
