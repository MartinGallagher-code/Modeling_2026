# Signetics 8X305 Processor Model

## Overview
- **Manufacturer**: Signetics
- **Year**: 1982
- **Architecture**: 8-bit Enhanced Bipolar Signal Processor
- **Technology**: Bipolar Schottky
- **Clock**: 8 MHz
- **Transistors**: ~5,000
- **Target CPI**: 2.0
- **Usage**: High-speed I/O-intensive signal processing

## Model Description
Grey-box queueing model for the Signetics 8X305, an enhanced bipolar signal processor designed for I/O-intensive applications. Featured fast single-cycle ALU with multi-cycle transfer and I/O operations.

## Instruction Categories
| Category | Cycles | Description |
|----------|--------|-------------|
| alu      | 1      | Single-cycle register ALU ops |
| transfer | 2      | Data transfer operations |
| io       | 3      | I/O bus operations |
| control  | 2      | Branch and conditional ops |
| memory   | 3      | External memory access |

## Validation Status
- **Status**: PASSED
- **CPI Error**: 0.00%
- **Last Validated**: 2026-01-29

## Files
- `current/signetics_8x305_validated.py` - Validated processor model
- `validation/signetics_8x305_validation.json` - Validation data and timing references
