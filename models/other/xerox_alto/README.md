# Xerox PARC Alto CPU Processor Model

## Overview
- **Manufacturer**: Xerox PARC
- **Year**: 1973
- **Architecture**: 16-bit TTL Custom, Bit-Serial ALU
- **Technology**: TTL custom
- **Clock**: 5.88 MHz
- **Target CPI**: 7.0
- **Usage**: Personal workstation with GUI, Ethernet, disk

## Model Description
Grey-box queueing model for the Xerox Alto CPU, the pioneering personal computer from Xerox PARC. Built from TTL logic with a bit-serial ALU, it integrated display refresh, disk, and Ethernet controllers via microcode tasks.

## Instruction Categories
| Category  | Cycles | Description |
|-----------|--------|-------------|
| alu       | 5      | Bit-serial ALU (16-bit, one bit at a time) |
| memory    | 8      | Memory access operations |
| control   | 6      | Control flow and microcode dispatch |
| display   | 10     | Display refresh and bitmap ops |
| disk      | 12     | Disk controller operations |
| ethernet  | 8      | Ethernet controller operations |

## Validation Status
- **Status**: PASSED
- **CPI Error**: 0.00%
- **Last Validated**: 2026-01-29

## Files
- `current/xerox_alto_validated.py` - Validated processor model
- `validation/xerox_alto_validation.json` - Validation data and timing references
