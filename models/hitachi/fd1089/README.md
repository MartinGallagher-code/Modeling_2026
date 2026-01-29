# Hitachi FD1089 Processor Model

## Overview
- **Manufacturer**: Hitachi (for Sega)
- **Year**: 1986
- **Type**: Encrypted Motorola 68000 variant
- **Clock**: 10 MHz
- **Transistors**: ~70000
- **Data Width**: 16-bit
- **Address Width**: 24-bit

## Description
The Hitachi FD1089 is an encrypted variant of the Motorola 68000 processor manufactured by Hitachi for Sega arcade systems. It contains the full 68000 instruction set internally but adds an on-die decryption layer that decodes encrypted opcodes during instruction fetch. Encryption keys are stored in battery-backed SRAM; if the battery dies, the key is lost and the chip becomes non-functional.

## Architecture
- Full Motorola 68000 core
- On-die opcode decryption logic
- Battery-backed key SRAM
- Substitution cipher encryption scheme
- Additional fetch latency due to decryption

## Usage
Used in Sega System 16 and other Sega arcade boards to prevent ROM copying and game piracy.

## Model Characteristics
- **Target CPI**: 7.0 (68000 base 6.5 + decrypt overhead)
- **Categories**: alu, data_transfer, memory, control, address, decrypt
- **Workloads**: typical, compute, memory_heavy, control_heavy

## Files
- `current/fd1089_validated.py` - Validated processor model
- `validation/fd1089_validation.json` - Validation data and sources
