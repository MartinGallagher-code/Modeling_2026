# TI Explorer Processor Model

## Overview
- **Manufacturer**: Texas Instruments
- **Year**: 1985
- **Architecture**: 32-bit Tagged LISP Machine CPU
- **Technology**: CMOS
- **Clock**: 8 MHz
- **Transistors**: ~80,000
- **Target CPI**: 4.0
- **Usage**: LISP machine CPU with pipelined microcode

## Model Description
Grey-box queueing model for the TI Explorer, Texas Instruments' LISP machine processor. Improved on the CADR design with pipelined microcode execution, reducing CPI for common LISP operations while maintaining tagged architecture support.

## Instruction Categories
| Category    | Cycles | Description |
|------------|--------|-------------|
| car_cdr     | 1      | Pipelined single-cycle CAR/CDR |
| cons        | 3      | Improved CONS allocation |
| eval        | 6      | Pipelined evaluation/dispatch |
| gc          | 10     | Garbage collection |
| memory      | 4      | Tagged memory read/write |
| type_check  | 2      | Improved hardware type checking |

## Validation Status
- **Status**: PASSED
- **CPI Error**: 0.00%
- **Last Validated**: 2026-01-29

## Files
- `current/ti_explorer_validated.py` - Validated processor model
- `validation/ti_explorer_validation.json` - Validation data and timing references
