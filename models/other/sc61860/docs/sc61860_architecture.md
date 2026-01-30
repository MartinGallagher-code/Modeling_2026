# Sharp SC61860 Architecture

## Overview

The Sharp SC61860 (also known as ESR-H predecessor) is a custom 8-bit CMOS CPU
designed by Sharp Corporation for their pocket computer product line. Introduced in
1980, it was the heart of several Sharp pocket computers including the PC-1211,
PC-1245, and PC-1500 series.

## Key Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1980 |
| Manufacturer | Sharp |
| Data Width | 8-bit |
| Address Space | 16-bit (64 KB) |
| Clock Speed | 576 kHz |
| Transistors | ~8,000 |
| Technology | CMOS |
| Internal RAM | 96 bytes |

## Architecture Details

### CPU Core

Accumulator-based 8-bit architecture with a relatively simple instruction set
optimized for running BASIC interpreters and simple programs on pocket computers.

### Register Set

- **A**: 8-bit accumulator
- **B**: 8-bit auxiliary register
- **I, J**: 8-bit index registers
- **DP**: 16-bit data pointer
- **PC**: 16-bit program counter
- **SP**: Stack pointer (internal RAM)
- **Flags**: Zero, Carry

### Internal Memory

- 96 bytes of internal RAM for registers, stack, and scratchpad
- 512 bytes of internal ROM for character generator patterns
- External ROM/RAM accessed via the address bus

### LCD Display Controller

Integrated LCD display controller capable of driving dot-matrix and segment
displays. Display operations involve writing pixel/segment data through
dedicated I/O ports, consuming more cycles than typical ALU operations.

### Instruction Set

- Arithmetic: ADD, SUB, INC, DEC, CMP
- Logic: AND, OR, XOR, NOT
- Data Transfer: LD, ST, MOV
- Control: JP, CALL, RET, conditional branches
- Display: LCD write, character output
- I/O: Port read/write

## Products Using SC61860

- Sharp PC-1211 (1980) - First pocket computer with the SC61860
- Sharp PC-1245 (1982) - Enhanced pocket BASIC computer
- Sharp PC-1500 (1981) - Advanced pocket computer with printer
- Sharp PC-1250 (1982) - Compact pocket computer
- Sharp EL-5500 (1982) - Scientific calculator variant

## Programming

The SC61860 ran a built-in BASIC interpreter stored in external ROM. Programs
were entered via the keyboard and stored in external RAM. The BASIC interpreter
dominated the instruction mix, with significant time spent in display update
routines.
