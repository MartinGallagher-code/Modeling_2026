# LMI Lambda Processor Model

## Overview
- **Manufacturer**: LISP Machines Inc.
- **Year**: 1984
- **Architecture**: 32-bit Tagged LISP Machine CPU
- **Technology**: TTL/MSI
- **Clock**: 4 MHz
- **Transistors**: ~60,000
- **Target CPI**: 5.0
- **Usage**: LISP machine CPU (CADR derivative)

## Model Description
Grey-box queueing model for the LMI Lambda, a CADR-derivative LISP machine CPU from LISP Machines Inc. Retained tagged architecture with hardware LISP support and modest improvements over the original CADR design.

## Instruction Categories
| Category    | Cycles | Description |
|------------|--------|-------------|
| car_cdr     | 2      | Hardware-assisted CAR/CDR |
| cons        | 4      | Improved CONS allocation |
| eval        | 7      | Microcoded evaluation/dispatch |
| gc          | 11     | Garbage collection |
| memory      | 5      | Tagged memory read/write |
| type_check  | 3      | Type tag checking |

## Validation Status
- **Status**: PASSED
- **CPI Error**: 0.00%
- **Last Validated**: 2026-01-29

## Files
- `current/lmi_lambda_validated.py` - Validated processor model
- `validation/lmi_lambda_validation.json` - Validation data and timing references
