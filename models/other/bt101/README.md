# Brooktree Bt101 Processor Model

## Overview
- **Manufacturer**: Brooktree
- **Year**: 1984
- **Architecture**: 8-bit RAMDAC
- **Technology**: CMOS
- **Clock**: 25 MHz
- **Transistors**: ~20,000
- **Target CPI**: 2.2
- **Usage**: Video display RAMDAC

## Model Description
Grey-box queueing model for the Brooktree Bt101, an early RAMDAC (Random Access Memory Digital-to-Analog Converter) used in video display systems. It integrated color palette RAM with DAC conversion for efficient pixel output.

## Instruction Categories
| Category     | Cycles | Description |
|-------------|--------|-------------|
| palette_read | 2      | Palette RAM read |
| dac_convert  | 3      | Digital-to-analog conversion |
| control      | 2      | Control and sync operations |
| pixel_clock  | 1      | Pixel clock synchronization |
| lookup       | 3      | Color lookup table operations |

## Validation Status
- **Status**: PASSED
- **CPI Error**: 0.00%
- **Last Validated**: 2026-01-29

## Files
- `current/bt101_validated.py` - Validated processor model
- `validation/bt101_validation.json` - Validation data and timing references
