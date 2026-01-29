# AT&T DSP-20 Processor Model

## Overview
- **Manufacturer**: AT&T Bell Labs
- **Year**: 1983
- **Architecture**: 16-bit Improved DSP
- **Technology**: NMOS
- **Clock**: 10 MHz
- **Target CPI**: 3.0

## Model Description
Grey-box queueing model for the AT&T DSP-20, an improved version of the DSP-1 developed at Bell Labs. The DSP-20 featured doubled clock speed and improved microcode efficiency, reducing CPI from 4.0 to 3.0 while maintaining focus on telecommunications signal processing.

## Instruction Categories
| Category  | Cycles | Description |
|-----------|--------|-------------|
| mac       | 2      | Multiply-accumulate (improved) |
| alu       | 2      | ALU operations |
| data_move | 2      | Data move operations |
| control   | 4      | Control flow |
| io        | 5      | I/O and peripherals |

## Validation Status
- **Status**: PASSED
- **CPI Error**: 1.67%
- **Last Validated**: 2026-01-29

## Files
- `current/att_dsp20_validated.py` - Validated processor model
- `validation/att_dsp20_validation.json` - Validation data and timing references
