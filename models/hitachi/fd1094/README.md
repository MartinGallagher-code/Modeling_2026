# Hitachi FD1094 Processor Model

## Overview
- **Manufacturer**: Hitachi (for Sega)
- **Year**: 1987
- **Type**: Improved encrypted Motorola 68000 variant
- **Clock**: 10 MHz
- **Transistors**: ~75000
- **Data Width**: 16-bit

## Description
The Hitachi FD1094 is an improved version of the FD1089 encrypted 68000 processor. It features a faster decryption engine and a more complex key schedule stored in 8KB of battery-backed SRAM. Like the FD1089, battery failure results in permanent key loss.

## Architecture
- Full Motorola 68000 core
- Enhanced decryption engine (faster than FD1089)
- 8KB battery-backed key SRAM
- State-dependent key schedule

## Usage
Used in Sega System 16B, System 18, and other later Sega arcade boards.

## Model Characteristics
- **Target CPI**: 6.8 (faster decrypt than FD1089's 7.0)
- **Categories**: alu, data_transfer, memory, control, address, decrypt
- **Workloads**: typical, compute, memory_heavy, control_heavy

## Files
- `current/fd1094_validated.py` - Validated processor model
- `validation/fd1094_validation.json` - Validation data and sources
