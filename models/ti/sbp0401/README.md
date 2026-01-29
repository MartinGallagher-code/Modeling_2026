# TI SBP0401 Processor Model

## Overview
- **Manufacturer**: Texas Instruments
- **Year**: 1975
- **Architecture**: 4-bit I2L Bit-Slice with Enhanced Control
- **Technology**: I2L (Integrated Injection Logic)
- **Transistors**: ~2000 per slice
- **Clock**: 10 MHz
- **Target CPI**: 3.0
- **Variant of**: SBP0400

## Model Description
Grey-box queueing model for the TI SBP0401, a variant of the SBP0400 with enhanced control logic. Maintains the same I2L process and performance characteristics while providing improved microcode sequencing capabilities.

## Instruction Categories
| Category | Cycles | Description |
|----------|--------|-------------|
| alu      | 2      | Arithmetic operations |
| shift    | 3      | Shift and rotate |
| logic    | 2      | Logic operations |
| control  | 4      | Enhanced microcode control |
| io       | 5      | I/O and bus interface |

## Validation Status
- **Status**: PASSED
- **CPI Error**: 0.0%
- **Last Validated**: 2026-01-29

## Files
- `current/sbp0401_validated.py` - Validated processor model
- `validation/sbp0401_validation.json` - Validation data and timing references
