# Intel 8087-2 Architecture Document

## Overview

| Property | Value |
|----------|-------|
| **Full Name** | Intel 8087-2 Numeric Data Processor |
| **Manufacturer** | Intel |
| **Year** | 1982 |
| **Process** | 3 um HMOS-II |
| **Transistors** | ~45,000 |
| **Clock Speed** | 8 MHz |
| **Data Width** | 80-bit internal |
| **Address Width** | 20-bit |
| **Package** | 40-pin DIP |

## Architecture Description

The Intel 8087-2 was a faster variant of the original 8087 FPU coprocessor. Operating at 8 MHz with approximately 20% fewer cycles per operation, it provided substantially improved floating-point throughput. It was designed for use with the 80286 and higher-speed 8086 systems.

### Execution Model

- **Type**: Sequential coprocessor
- **Pipeline**: None (fully sequential execution)
- **Register File**: 8 x 80-bit registers organized as a stack (ST(0)-ST(7))
- **Precision**: 80-bit extended, 64-bit double, 32-bit single

### Instruction Categories

| Category | Base Cycles | Description |
|----------|-------------|-------------|
| fp_add | 56 | Floating-point addition/subtraction (~20% faster than 8087) |
| fp_mul | 88 | Floating-point multiplication (~20% faster) |
| fp_div | 160 | Floating-point division (~20% faster) |
| fp_sqrt | 144 | Square root (~20% faster) |
| fld_fst | 16 | Load/store stack operations (~20% faster) |
| fxch | 12 | Register exchange (~20% faster) |

### Improvements over 8087

- Higher clock speed: 8 MHz vs 5 MHz
- Reduced cycle counts: ~20% fewer cycles per operation
- Combined throughput improvement: ~2.5x over original 8087
- Full instruction set compatibility

### Key Features

- Identical instruction set to 8087
- 80-bit extended precision
- IEEE 754 compatible arithmetic
- Stack-based register architecture
- Improved HMOS-II process technology

## References

- Intel 8087-2 Data Sheet (1982)
- Intel iAPX 286 Hardware Reference Manual
- Wikipedia: Intel 8087
