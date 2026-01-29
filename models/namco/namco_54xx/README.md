# Namco 54xx Processor Model

## Overview
- **Manufacturer**: Namco
- **Year**: 1981
- **Type**: Custom 4-bit sound generator
- **Clock**: 1.5 MHz
- **Transistors**: ~3000
- **Data Width**: 4-bit

## Description
The Namco 54xx is a custom sound generator chip used in Namco arcade games. It provides LFSR-based noise generation, waveform synthesis, multi-channel mixing, and DAC output for producing explosions, engine noise, and other sound effects.

## Architecture
- LFSR noise generator
- Waveform table lookup synthesis
- Multi-channel audio mixing
- DAC output stage
- Command-driven state machine

## Usage
Used in Galaga, Bosconian, Dig Dug, and other Namco arcade boards for sound effect generation.

## Model Characteristics
- **Target CPI**: 6.0
- **Categories**: noise_gen, waveform, mix, io, control, dac
- **Workloads**: typical, noise_heavy, waveform_heavy, idle

## Files
- `current/namco_54xx_validated.py` - Validated processor model
- `validation/namco_54xx_validation.json` - Validation data and sources
