# Namco 53xx Processor Model

## Overview
- **Manufacturer**: Namco
- **Year**: 1981
- **Type**: Custom 4-bit multiplexer
- **Clock**: 1.5 MHz
- **Transistors**: ~1500
- **Data Width**: 4-bit

## Description
The Namco 53xx is the simplest of the Namco custom chips, serving as an input multiplexer. It selects between multiple input sources and routes data to the main CPU, handling channel selection and synchronization.

## Architecture
- Simple multiplexer with channel selection
- Minimal state machine
- Synchronization timing
- Sequential execution

## Usage
Used in Pole Position, Phozon, and other Namco arcade boards for input multiplexing.

## Model Characteristics
- **Target CPI**: 4.0
- **Categories**: mux_select, data_transfer, io, control, timing
- **Workloads**: typical, high_throughput, idle

## Files
- `current/namco_53xx_validated.py` - Validated processor model
- `validation/namco_53xx_validation.json` - Validation data and sources
