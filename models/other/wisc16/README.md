# WISC CPU/16 Processor Model

## Overview
- **Designer**: Phil Koopman (Carnegie Mellon University)
- **Year**: 1986
- **Type**: 16-bit Writable Instruction Set Computer (stack machine)
- **Clock**: 4 MHz
- **Construction**: TTL discrete logic
- **Data Width**: 16-bit

## Description
The WISC CPU/16 is a research stack machine designed by Phil Koopman. Its defining feature is a fully RAM-based writable microcode store, allowing the instruction set to be redefined at runtime. Built from TTL discrete logic on wire-wrap boards, it demonstrates the feasibility of user-customizable instruction sets.

## Architecture
- Stack-oriented (zero-operand) instruction format
- Writable control store (RAM-based microcode)
- Hardware data stack and return stack
- Forth-oriented design
- TTL discrete logic construction

## Usage
Research platform for exploring writable instruction sets, stack machine architectures, and Forth language implementations.

## Model Characteristics
- **Target CPI**: 2.5
- **Categories**: stack_ops, alu, memory, control, microcode
- **Workloads**: typical, compute, stack_heavy, custom_isa

## Files
- `current/wisc16_validated.py` - Validated processor model
- `validation/wisc16_validation.json` - Validation data and sources
