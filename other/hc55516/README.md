# Harris HC-55516 Processor Model

## Overview
- **Manufacturer**: Harris
- **Year**: 1982
- **Type**: CVSD audio codec
- **Clock**: 2 MHz
- **Transistors**: ~1500
- **Data Width**: 1-bit (CVSD)

## Description
The Harris HC-55516 is a CVSD (Continuously Variable Slope Delta) audio codec used in Williams arcade games and pinball machines. It decodes single-bit CVSD-compressed audio streams into analog audio output, providing speech and sound effects from highly compressed digital data.

## Architecture
- Single-bit CVSD input stream
- Adaptive slope delta modulation decoder
- Syllabic filter / integrator
- DAC analog output
- Very simple processing pipeline

## Usage
Used in Williams arcade games (Defender, Robotron, Sinistar) and Williams/Bally pinball machines for digitized speech and sound effects.

## Model Characteristics
- **Target CPI**: 2.0
- **Categories**: decode, filter, dac, control, timing
- **Workloads**: typical, continuous, idle

## Files
- `current/hc55516_validated.py` - Validated processor model
- `validation/hc55516_validation.json` - Validation data and sources
