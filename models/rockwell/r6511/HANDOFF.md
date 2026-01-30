# Rockwell R6511 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: <5%
- **Last Updated**: 2026-01-29

## Current Model Summary
- Architecture: 8-bit NMOS microcontroller (6502-based)
- Year: 1980
- Clock: 2.0 MHz
- Target CPI: 3.0 (same as 6502)
- Instruction categories: Same as MOS 6502

Key instruction categories:
| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 2.3 | ALU operations |
| data_transfer | 2.8 | Load/store immediate and register |
| memory | 4.0 | Memory access with addressing modes |
| control | 2.6 | Branch and jump |
| stack | 3.5 | Push/pop and subroutine calls |

## Cross-Validation Status
- **Identical timing**: MOS 6502, Rockwell R6500 series
- **Related processors**: MOS 6510, WDC 65C02
- **Timing rule**: Same as 6502 datasheet

## Known Issues
- None - model uses validated 6502 timing

## Suggested Next Steps
- Model is complete based on 6502 timing
- Could add specific workload profiles for peripheral I/O heavy applications

## Key Architectural Notes
- The Rockwell R6511 was part of the R6500 family of 6502 derivatives
- Integrated peripherals: parallel I/O, serial I/O, timer/counter
- On-chip RAM (64-128 bytes depending on variant)
- On-chip ROM (1-4KB depending on variant)
- Used in industrial control, consumer electronics, and automotive applications

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 5
- **Corrections**: See `identification/sysid_result.json`
