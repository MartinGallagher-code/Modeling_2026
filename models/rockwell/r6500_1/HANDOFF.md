# Rockwell R6500/1 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 3.33%
- **Last Updated**: 2026-01-29
- **Cross-validation**: Initial validation complete

## Current Model Summary
- Architecture: 8-bit MCU, 6502 core, sequential execution
- Clock: 1.0 MHz
- Target CPI: 3.0
- Predicted CPI: 2.90

Key instruction categories:
| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 2 | ALU operations (ADC, SBC, AND, ORA) |
| data_transfer | 3 | Data transfer (LDA, STA, TAX) |
| memory | 4 | Memory operations (indirect, indexed) |
| control | 3 | Control flow (BNE, JMP, JSR) |
| stack | 3 | Stack operations (PHA, PLA) |

## Cross-Validation Summary
- Per-instruction tests: 10 tests, all passing
- Reference sources: MOS 6502 Programming Manual, Rockwell R6500 Data Sheet

## Known Issues
- None - model uses well-documented 6502 timing

## Suggested Next Steps
- Compare with other 6502-family MCUs (R6511, etc.)

## Key Architectural Notes
- Rockwell R6500/1 (1978) - single-chip 6502 MCU
- 2KB on-chip ROM, 64 bytes on-chip RAM
- On-chip I/O ports and programmable timer
- Identical instruction timing to MOS 6502
- Used in consumer electronics, industrial control, point-of-sale
