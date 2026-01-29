# Namco 51xx Processor Model

## Overview
- **Manufacturer**: Namco
- **Year**: 1981
- **Type**: Custom 4-bit I/O controller
- **Clock**: 1.5 MHz
- **Transistors**: ~2000
- **Data Width**: 4-bit

## Description
The Namco 51xx is a custom 4-bit I/O controller chip used in Namco arcade games for handling coin switch inputs, joystick direction multiplexing, and credit management. It performs switch debouncing and communicates with the main CPU via a command/response protocol.

## Architecture
- Simple state machine design
- Coin switch debouncing logic
- Joystick direction multiplexer
- Credit counting and management
- Sequential execution

## Usage
Used in Pac-Man, Galaga, Bosconian, and other Namco arcade boards to offload I/O handling from the main Z80 CPU.

## Model Characteristics
- **Target CPI**: 5.0
- **Categories**: alu, data_transfer, io, control, debounce
- **Workloads**: typical, input_heavy, coin_insert, idle

## Files
- `current/namco_51xx_validated.py` - Validated processor model
- `validation/namco_51xx_validation.json` - Validation data and sources
