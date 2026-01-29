# Namco 50xx Processor Model

## Overview
- **Manufacturer**: Namco
- **Year**: 1981
- **Type**: Custom 4-bit state machine
- **Clock**: 1.5 MHz
- **Transistors**: ~2000
- **Data Width**: 4-bit

## Description
The Namco 50xx is a custom 4-bit chip used for score calculation and coin handling in Pac-Man era Namco arcade games. It operates as a simple state machine that manages player scores, high scores, and coin/credit counting.

## Architecture
- Simple state machine design
- No general-purpose instruction set
- Fixed command/response protocol with main CPU
- Sequential execution

## Usage
Used in classic Namco arcade boards including Pac-Man, Galaga, and Dig Dug for offloading score and coin management from the main Z80 CPU.

## Model Characteristics
- **Target CPI**: 5.0
- **Categories**: alu, data_transfer, io, control, timer
- **Workloads**: typical, scoring, coin_handling, idle

## Files
- `current/namco_50xx_validated.py` - Validated processor model
- `validation/namco_50xx_validation.json` - Validation data and sources
