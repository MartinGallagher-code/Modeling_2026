# Nippon Columbia CX-1 Processor Model

## Overview
- **Manufacturer**: Nippon Columbia
- **Year**: 1983
- **Architecture**: 16-bit Arcade Audio DSP
- **Technology**: NMOS
- **Clock**: 5 MHz
- **Transistors**: ~15,000
- **Target CPI**: 3.0
- **Usage**: Arcade sound generation and audio filtering

## Model Description
Grey-box queueing model for the Nippon Columbia CX-1, a custom audio DSP used in arcade machines. Sequential architecture optimized for audio filter operations and waveform generation.

## Instruction Categories
| Category | Cycles | Description |
|----------|--------|-------------|
| mac      | 2      | Multiply-accumulate (sequential) |
| filter   | 4      | Audio filter coefficient operations |
| output   | 3      | Audio output and DAC |
| control  | 3      | Control flow and loops |
| memory   | 4      | Sample buffer and coefficient access |

## Validation Status
- **Status**: PASSED
- **CPI Error**: 0.00%
- **Last Validated**: 2026-01-29

## Files
- `current/cx1_validated.py` - Validated processor model
- `validation/cx1_validation.json` - Validation data and timing references
