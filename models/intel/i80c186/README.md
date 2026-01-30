# Intel 80C186

## Quick Reference
| Parameter | Value |
|-----------|-------|
| Year | 1982 |
| Type | CMOS embedded 16-bit CPU |
| Clock | 8 MHz |
| Transistors | ~55,000 |
| Process | CMOS |
| Data Bus | 16-bit |
| Address Bus | 20-bit (1MB) |
| Architecture | x86 (8086 superset) |

## Description
The 80C186 is the CMOS version of the Intel 80186, an embedded variant of the 8086.
It integrates clock generator, interrupt controller, DMA controller, timers, and
chip select logic on a single chip. Same instruction set and timing as the 80186
but with significantly lower power consumption. Billions shipped, primarily used
in networking equipment (modems, routers, telecommunications).

## Validation Status
- **Status**: PASSED
- **CPI Error**: 0.9%
- **Model CPI**: 5.943 (target: 6.0)
- **Last Validated**: 2026-01-29

## Instruction Categories
| Category | Cycles | Description |
|----------|--------|-------------|
| ALU | 3 | ADD, SUB, AND, OR, XOR, CMP |
| Data Transfer | 2 | MOV, XCHG register ops |
| Memory | 8 | Load/store with addressing modes |
| Control | 8 | JMP, CALL, RET, branches |
| Stack | 8 | PUSH, POP, PUSHA, POPA |
| Multiply | 25 | MUL, IMUL, DIV, IDIV |

## Key Differences from 80186
- CMOS process (lower power, wider voltage range)
- Same instruction timing
- Same integrated peripherals
- Used in embedded/networking rather than PC applications
