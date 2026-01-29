# Namco 52xx Processor Model

## Overview
- **Manufacturer**: Namco
- **Year**: 1981
- **Type**: Custom 4-bit sample playback chip
- **Clock**: 1.5 MHz
- **Transistors**: ~3000
- **Data Width**: 4-bit

## Description
The Namco 52xx is a custom chip for digital audio sample playback used in Namco arcade games. It fetches sample data via DMA from ROM and drives a DAC for analog audio output, providing sound effects like explosions and speech.

## Architecture
- DMA-style sample fetching from ROM
- Sample decode and processing pipeline
- DAC output stage
- State machine control for playback sequencing
- Sample rate timing control

## Usage
Used in Bosconian, Galaga, Pole Position, and other Namco arcade boards for digital audio sample playback.

## Model Characteristics
- **Target CPI**: 6.0
- **Categories**: audio_dma, sample_read, dac, control, timing
- **Workloads**: typical, playback, idle, multi_sample

## Files
- `current/namco_52xx_validated.py` - Validated processor model
- `validation/namco_52xx_validation.json` - Validation data and sources
