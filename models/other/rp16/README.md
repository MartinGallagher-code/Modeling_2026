# Raytheon RP-16 Processor Model

## Overview
- **Manufacturer**: Raytheon
- **Year**: 1978
- **Architecture**: 16-bit Military Bit-Slice System
- **Technology**: Military-grade bipolar
- **Implementation**: 7-chip system
- **Clock**: 10 MHz
- **Target CPI**: 4.0

## Model Description
Grey-box queueing model for the Raytheon RP-16 military-grade bit-slice processor system. The RP-16 was a 7-chip 16-bit system designed for defense and aerospace applications, prioritizing reliability and radiation hardening over maximum speed.

## Instruction Categories
| Category | Cycles | Description |
|----------|--------|-------------|
| alu      | 3      | 16-bit ALU operations |
| shift    | 3      | Shift and rotate |
| logic    | 3      | Logic operations |
| control  | 5      | Control/branch (multi-chip overhead) |
| memory   | 6      | Memory access (4 base + 2 memory) |

## Validation Status
- **Status**: PASSED
- **CPI Error**: 1.25%
- **Last Validated**: 2026-01-29

## Files
- `current/rp16_validated.py` - Validated processor model
- `validation/rp16_validation.json` - Validation data and timing references
