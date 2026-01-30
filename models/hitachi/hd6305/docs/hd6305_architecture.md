# Hitachi HD6305 Architecture

## Overview
The Hitachi HD6305 (1983) is a CMOS 8-bit microcontroller, second-source compatible with the Motorola 6805 family, featuring enhanced timer/counter peripherals.

## Key Features
- 8-bit data bus, 13-bit address bus
- 4 MHz clock frequency
- ~10,000 CMOS transistors
- 6805 instruction set compatible
- Enhanced timer/counter units
- Low-power CMOS operation

## Instruction Categories
| Category | Cycles | Description |
|----------|--------|-------------|
| ALU | 3 | Basic arithmetic and logic |
| Data Transfer | 3 | Load/store operations |
| Memory | 5 | Extended/indexed memory access |
| Control | 4 | Branch, jump, subroutine call |
| Timer | 4 | Timer capture/compare/output |

## Application
Embedded control applications:
- Automotive sub-systems
- Consumer electronics
- Industrial sensor interfaces
- Timer-based control loops

## Related Processors
- Motorola 6805 (original design)
- Motorola 6805R2 (appliance variant)
- Motorola 68HC05 (CMOS successor)
