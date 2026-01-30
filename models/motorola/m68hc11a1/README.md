# Motorola 68HC11A1

## Quick Reference
| Parameter | Value |
|-----------|-------|
| Year | 1984 |
| Type | 8-bit Microcontroller |
| E Clock | 2 MHz (8 MHz crystal / 4) |
| Transistors | ~120,000 |
| Process | HCMOS |
| Data Bus | 8-bit |
| Address Bus | 16-bit (64KB) |
| ROM | 8KB |
| RAM | 256 bytes |
| EEPROM | 512 bytes |

## Description
The 68HC11A1 is the most popular variant of the Motorola 68HC11 family.
It extends the 6800 instruction set with a Y index register, 16-bit math
(MUL, IDIV, FDIV), and bit manipulation instructions (BSET, BCLR, BRSET,
BRCLR). It includes SCI, SPI, timer, A/D converter, and other peripherals.
All I/O is memory-mapped. Timing is based on the E clock (crystal / 4).

## Validation Status
- **Status**: PASSED
- **CPI Error**: 0.0%
- **Model CPI**: 4.498 (target: 4.5)
- **Last Validated**: 2026-01-29

## Instruction Categories
| Category | Cycles | Description |
|----------|--------|-------------|
| Inherent | 2 | NOP, INX, DEX, CLC |
| Immediate | 2 | LDAA #imm, ADDA #imm |
| Direct | 4 | Direct page (LDAA ) |
| Extended | 5 | Extended (LDAA ) |
| Indexed | 5 | Indexed (LDAA n,X) |
| Branch | 4 | BEQ, BNE, BCC |
| Jump/Call | 8 | JSR, BSR, RTS, JMP |
| Stack | 5 | PSHA, PULA, PSHX |
| Multiply | 12 | MUL, IDIV, FDIV |
| Bit Manipulation | 7 | BSET, BCLR, BRSET |
| I/O Peripheral | 5 | Memory-mapped I/O |
