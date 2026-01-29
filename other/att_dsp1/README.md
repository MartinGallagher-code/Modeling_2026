# AT&T DSP-1 Processor Model

## Overview
- **Manufacturer**: AT&T Bell Labs
- **Year**: 1980
- **Architecture**: 16-bit Early DSP
- **Technology**: NMOS
- **Clock**: 5 MHz
- **Target CPI**: 4.0
- **Usage**: Captive/internal Bell Labs use (not commercially sold)

## Model Description
Grey-box queueing model for the AT&T DSP-1, one of the earliest digital signal processors developed at Bell Labs. This was an internal design used in AT&T telecommunications equipment, not commercially available. Its microcoded architecture resulted in relatively high CPI compared to later commercial DSPs.

## Instruction Categories
| Category  | Cycles | Description |
|-----------|--------|-------------|
| mac       | 3      | Multiply-accumulate (no hardware MAC) |
| alu       | 3      | ALU operations |
| data_move | 3      | Data move operations |
| control   | 5      | Control flow |
| io        | 6      | I/O and peripherals |

## Validation Status
- **Status**: PASSED
- **CPI Error**: 1.25%
- **Last Validated**: 2026-01-29

## Files
- `current/att_dsp1_validated.py` - Validated processor model
- `validation/att_dsp1_validation.json` - Validation data and timing references
