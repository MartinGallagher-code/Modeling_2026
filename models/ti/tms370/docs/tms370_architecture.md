# TI TMS370 Architecture

## Overview
The TI TMS370 (1985) is an 8-bit industrial microcontroller featuring a register-file based architecture, designed for process control and industrial automation.

## Key Features
- 8-bit data bus, 16-bit address bus
- 8 MHz clock frequency
- ~30,000 CMOS transistors
- Register-file architecture (not accumulator-based)
- Rich on-chip peripheral set
- Multiple timer/counter units

## Instruction Categories
| Category | Cycles | Description |
|----------|--------|-------------|
| ALU | 2 | Register-to-register arithmetic/logic |
| Data Transfer | 3 | Register/memory data moves |
| Memory | 4 | Extended memory access |
| Control | 3 | Branch, call, return |
| Peripheral | 5 | Peripheral register read/write |

## Application
Designed for industrial control:
- PLC (Programmable Logic Controller) front-ends
- Motor control
- Process instrumentation
- Industrial communication interfaces

## Related Processors
- TI TMS320 (DSP family, different architecture)
- TI MSP430 (later low-power MCU successor concept)
