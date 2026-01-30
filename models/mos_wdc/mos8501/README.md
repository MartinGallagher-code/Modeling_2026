# MOS 8501

## Quick Reference
| Parameter | Value |
|-----------|-------|
| Year | 1984 |
| Type | 8-bit CPU |
| Clock | 1.76 MHz (PAL) |
| Transistors | ~7,000 |
| Process | HMOS |
| Data Bus | 8-bit |
| Address Bus | 16-bit (64KB) |
| ISA | 6502 |

## Description
The MOS 8501 is an HMOS variant of the MOS 6502 with an integrated clock
generator. It was used as the CPU in the Commodore C16 and Plus/4 computers.
Functionally identical to the 6502 instruction set with 2-7 cycle instruction
timings depending on addressing mode.

## Validation Status
- **Status**: PASSED
- **CPI Error**: 2.0%
- **Model CPI**: 3.724 (target: 3.80)
- **Last Validated**: 2026-01-29

## Instruction Categories
| Category | Cycles | Description |
|----------|--------|-------------|
| ALU | 2.8 | ADC, SBC, AND, ORA, EOR, CMP |
| Data Transfer | 3.7 | LDA, STA, LDX, STX |
| Memory (RMW) | 5.0 | INC, DEC, ASL, LSR, ROL, ROR |
| Control | 3.8 | JMP, JSR, RTS, Bxx |
| Stack | 4.0 | PHA, PLA, PHP, PLP |
