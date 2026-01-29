# WISC CPU/32 Processor Model

## Overview
- **Designer**: Phil Koopman (Carnegie Mellon University)
- **Year**: 1988
- **Type**: 32-bit Writable Instruction Set Computer (stack machine)
- **Clock**: 8 MHz
- **Construction**: TTL discrete logic
- **Data Width**: 32-bit

## Description
The WISC CPU/32 is the 32-bit evolution of the WISC CPU/16 research stack machine. It features a wider data path, faster clock, and improved microcode engine, resulting in lower CPI than its predecessor while maintaining the writable instruction set capability.

## Architecture
- 32-bit stack-oriented instruction format
- Writable control store (RAM-based microcode)
- Hardware data stack and return stack
- Improved microcode engine
- TTL discrete logic construction

## Model Characteristics
- **Target CPI**: 2.0 (improved from CPU/16's 2.5)
- **Categories**: stack_ops, alu, memory, control, microcode
- **Workloads**: typical, compute, stack_heavy, custom_isa

## Files
- `current/wisc32_validated.py` - Validated processor model
- `validation/wisc32_validation.json` - Validation data and sources
