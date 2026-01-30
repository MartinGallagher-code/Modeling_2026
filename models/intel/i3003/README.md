# Intel 3003 Processor Model

## Overview
- **Manufacturer**: Intel
- **Year**: 1975
- **Architecture**: 2-bit Carry Lookahead Generator
- **Technology**: Schottky bipolar
- **Clock**: 10 MHz
- **Transistors**: ~100
- **Target CPI**: 1.0
- **Usage**: Carry lookahead for Intel 3002 bit-slice ALU

## Model Description
Grey-box queueing model for the Intel 3003 carry lookahead generator. All operations complete in a single cycle, generating carry signals in parallel for fast multi-bit arithmetic with Intel 3002 bit-slice ALUs.

## Instruction Categories
| Category     | Cycles | Description |
|-------------|--------|-------------|
| carry_gen    | 1      | Parallel carry generation |
| propagate    | 1      | Carry propagation signals |
| group_carry  | 1      | Group carry for cascade |
| control      | 1      | Mode selection |

## Validation Status
- **Status**: PASSED
- **CPI Error**: 0.00%
- **Last Validated**: 2026-01-29

## Files
- `current/i3003_validated.py` - Validated processor model
- `validation/i3003_validation.json` - Validation data and timing references
