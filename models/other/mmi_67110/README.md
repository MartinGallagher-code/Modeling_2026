# MMI 67110 Processor Model

## Overview
- **Manufacturer**: Monolithic Memories Inc.
- **Year**: 1978
- **Architecture**: 4-bit Enhanced Bit-Slice Sequencer
- **Technology**: Bipolar Schottky
- **Clock**: 10 MHz
- **Transistors**: ~3,000
- **Target CPI**: 1.8
- **Usage**: Microprogram sequencer for bit-slice systems

## Model Description
Grey-box queueing model for the MMI 67110, an enhanced microprogram sequencer for bit-slice processor systems. Provided sequencing, branching, subroutine calls, and loop counting for custom processor designs.

## Instruction Categories
| Category   | Cycles | Description |
|-----------|--------|-------------|
| sequence   | 1      | Sequential address generation |
| branch     | 2      | Conditional/unconditional branch |
| subroutine | 3      | Call/return with stack |
| control    | 2      | Control and mode operations |
| counter    | 1      | Loop counter operations |

## Validation Status
- **Status**: PASSED
- **CPI Error**: 0.00%
- **Last Validated**: 2026-01-29

## Files
- `current/mmi_67110_validated.py` - Validated processor model
- `validation/mmi_67110_validation.json` - Validation data and timing references
