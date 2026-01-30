# Symbolics CADR Processor Model

## Overview
- **Manufacturer**: Symbolics (MIT AI Lab)
- **Year**: 1981
- **Architecture**: 32-bit Tagged LISP Machine CPU
- **Technology**: TTL/MSI
- **Clock**: 5 MHz
- **Transistors**: ~50,000
- **Target CPI**: 5.5
- **Usage**: LISP machine CPU with native LISP operations

## Model Description
Grey-box queueing model for the Symbolics CADR, the CPU of the CADR LISP machine developed at the MIT AI Lab. Featured microcoded architecture with tagged data types, hardware CAR/CDR operations, and hardware-assisted garbage collection.

## Instruction Categories
| Category    | Cycles | Description |
|------------|--------|-------------|
| car_cdr     | 2      | Hardware-assisted CAR/CDR list operations |
| cons        | 5      | CONS cell allocation |
| eval        | 8      | Evaluation/function dispatch |
| gc          | 12     | Garbage collection operations |
| memory      | 6      | Tagged memory read/write |
| type_check  | 3      | Type tag checking and dispatch |

## Validation Status
- **Status**: PASSED
- **CPI Error**: 0.00%
- **Last Validated**: 2026-01-29

## Files
- `current/symbolics_cadr_validated.py` - Validated processor model
- `validation/symbolics_cadr_validation.json` - Validation data and timing references
