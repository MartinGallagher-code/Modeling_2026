# TI SBP0400 Processor Model

## Overview
- **Manufacturer**: Texas Instruments
- **Year**: 1975
- **Architecture**: 4-bit I2L Bit-Slice, cascadable to 16-bit
- **Technology**: I2L (Integrated Injection Logic)
- **Transistors**: ~2000 per slice
- **Clock**: 10 MHz
- **Target CPI**: 3.0

## Model Description
Grey-box queueing model for the TI SBP0400 bit-slice processor. The SBP0400 used TI's Integrated Injection Logic process, offering a balance between speed and power consumption compared to Schottky TTL alternatives like the AMD Am2901.

## Instruction Categories
| Category | Cycles | Description |
|----------|--------|-------------|
| alu      | 2      | Arithmetic operations |
| shift    | 3      | Shift and rotate |
| logic    | 2      | Logic operations |
| control  | 4      | Microcode control/sequencing |
| io       | 5      | I/O and bus interface |

## Validation Status
- **Status**: PASSED
- **CPI Error**: 0.0%
- **Last Validated**: 2026-01-29

## Files
- `current/sbp0400_validated.py` - Validated processor model
- `validation/sbp0400_validation.json` - Validation data and timing references
