# Intel 8087 Architecture Document

## Overview

| Property | Value |
|----------|-------|
| **Full Name** | Intel 8087 Numeric Data Processor |
| **Manufacturer** | Intel |
| **Year** | 1980 |
| **Process** | 3 um HMOS |
| **Transistors** | ~45,000 |
| **Clock Speed** | 5 MHz |
| **Data Width** | 80-bit internal |
| **Address Width** | 20-bit |
| **Package** | 40-pin DIP |

## Architecture Description

The Intel 8087 was the first x87 floating-point coprocessor, designed to accelerate floating-point arithmetic for the 8086/8088 processor family. It introduced the x87 instruction set that would remain compatible through all subsequent x86 FPU implementations.

### Execution Model

- **Type**: Sequential coprocessor
- **Pipeline**: None (fully sequential execution)
- **Register File**: 8 x 80-bit registers organized as a stack (ST(0)-ST(7))
- **Precision**: 80-bit extended, 64-bit double, 32-bit single

### Instruction Categories

| Category | Base Cycles | Description |
|----------|-------------|-------------|
| fp_add | 70 | Floating-point addition/subtraction |
| fp_mul | 110 | Floating-point multiplication |
| fp_div | 200 | Floating-point division |
| fp_sqrt | 180 | Square root |
| fld_fst | 20 | Load/store stack operations |
| fxch | 15 | Register exchange |

### Coprocessor Interface

The 8087 monitors the host CPU bus for coprocessor instructions (ESC opcodes). When detected, the 8087 takes over execution while the host CPU enters a wait state. The BUSY/WAIT protocol synchronizes operations between the two processors.

### Key Features

- 80-bit extended precision (64-bit mantissa, 15-bit exponent)
- IEEE 754 compatible arithmetic (predates final standard)
- Hardware support for transcendental functions
- Stack-based register architecture
- Shared bus with host processor

## References

- Intel 8087 Data Sheet (1980)
- Intel iAPX 86/88, 186/188 User's Manual
- Wikipedia: Intel 8087
