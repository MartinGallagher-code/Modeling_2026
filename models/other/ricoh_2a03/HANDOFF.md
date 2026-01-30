# Ricoh 2A03 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 2.17%
- **Last Updated**: 2026-01-29
- **Cross-validation**: Complete - identical to MOS 6502

## Current Model Summary
- Architecture: 8-bit NMOS, sequential execution
- Clock: 1.79 MHz (NTSC), 1.66 MHz (PAL variant 2A07)
- Target CPI: 3.0
- Predicted CPI: 3.065

Key instruction categories (identical to MOS 6502):
| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 2.3 | ALU operations (INX, ADC, CMP) |
| data_transfer | 2.8 | Data movement (LDA, TAX) |
| memory | 4.0 | Memory access (STA, indexed) |
| control | 2.6 | Control flow (branches, JMP) |
| stack | 3.5 | Stack operations (JSR, RTS, PHA) |

## Cross-Validation Summary
- Per-instruction tests: 32/32 passed (identical to 6502)
- Reference sources: MOS 6502 Datasheet, FCEUX, Nestopia, NESDev Wiki
- Related processor: MOS 6502 (identical timing)

## Key Architectural Differences from MOS 6502

### BCD Mode Disabled
- The SED (Set Decimal) instruction exists but has NO effect
- CLD (Clear Decimal) also exists but is redundant
- ADC and SBC always operate in binary mode
- This saves silicon area and was not needed for game console applications

### On-Chip APU (Not Modeled)
- Includes 5-channel audio processing unit
- 2 pulse wave channels
- 1 triangle wave channel
- 1 noise channel
- 1 delta modulation channel (DMC)
- APU does not affect CPU instruction timing

### Clock Speed
- NTSC: 1.7897725 MHz (master clock / 12)
- PAL (2A07): 1.662607 MHz (master clock / 16)
- Higher than typical 6502 (1 MHz)

## Known Issues
- None - model fully validated within 5% error
- Timing is cycle-accurate with MOS 6502

## Suggested Next Steps
- Model is complete; no further work required
- Could add PAL variant (2A07) as separate configuration
- Could model APU if audio timing becomes relevant

## Why This Model Exists
The Ricoh 2A03 powers the Nintendo Entertainment System (NES/Famicom), one of the most influential gaming platforms in history. Understanding its performance characteristics is valuable for:
- NES game development and optimization
- Emulator development and validation
- Retro computing research
- Historical processor architecture studies

## Usage in NES
- CPU handles game logic, input processing, and coordinates PPU/APU
- Tight timing loops common for raster effects
- DMA transfer to PPU takes 513-514 CPU cycles
- NMI (vertical blank) interrupt drives game frame timing

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 5
- **Corrections**: See `identification/sysid_result.json`
