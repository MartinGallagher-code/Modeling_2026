# AMI S28211 Processor Model

## Overview
- **Manufacturer**: AMI
- **Year**: 1979
- **Architecture**: DSP Peripheral for Motorola 6800 Bus
- **Technology**: NMOS
- **Transistors**: ~5000
- **Clock**: 8 MHz
- **Target CPI**: 5.0

## Model Description
Grey-box queueing model for the AMI S28211, a DSP peripheral chip designed for the Motorola 6800 bus. Unlike standalone DSPs, the S28211 operated as a coprocessor/peripheral, adding signal processing capability to 6800-based systems. The bus interface overhead contributes to higher CPI compared to standalone DSPs.

## Instruction Categories
| Category  | Cycles | Description |
|-----------|--------|-------------|
| mac       | 4      | Multiply-accumulate (no hardware MAC) |
| alu       | 3      | ALU operations |
| data_move | 4      | Data move via 6800 bus |
| control   | 6      | Control flow |
| io        | 8      | I/O through 6800 bus (high overhead) |

## Validation Status
- **Status**: PASSED
- **CPI Error**: 1.0%
- **Last Validated**: 2026-01-29

## Files
- `current/ami_s28211_validated.py` - Validated processor model
- `validation/ami_s28211_validation.json` - Validation data and timing references
