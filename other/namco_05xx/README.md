# Namco 05xx Processor Model

## Overview
- **Manufacturer**: Namco
- **Year**: 1981
- **Type**: Custom 4-bit starfield generator
- **Clock**: 1.5 MHz
- **Transistors**: ~2000
- **Data Width**: 4-bit

## Description
The Namco 05xx is a custom chip responsible for generating the iconic scrolling starfield backgrounds seen in Galaga, Bosconian, and other Namco arcade games. It calculates star positions, handles scroll offsets for parallax effects, and outputs pixel data synchronized to the video timing.

## Architecture
- Star position calculation engine
- Pixel output to video hardware
- Scroll offset for parallax layers
- Video sync timing
- Sequential execution state machine

## Usage
Used in Galaga, Bosconian, and other Namco arcade boards for starfield background rendering.

## Model Characteristics
- **Target CPI**: 4.0
- **Categories**: star_calc, pixel_out, scroll, control, timing
- **Workloads**: typical, dense_field, scrolling, idle

## Files
- `current/namco_05xx_validated.py` - Validated processor model
- `validation/namco_05xx_validation.json` - Validation data and sources
