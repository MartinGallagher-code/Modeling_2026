# Harris RTX32P Architecture

## Overview
The Harris RTX32P (1985) is a 32-bit pipelined Forth stack processor with hardware dual stacks, designed for high-performance Forth execution in real-time and embedded applications.

## Key Features
- 32-bit data bus and address bus
- 8 MHz clock frequency
- ~40,000 CMOS transistors
- Pipelined execution
- Hardware data stack (256 deep)
- Hardware return stack (256 deep)
- Single-cycle Forth primitives
- Hardware subroutine threading

## Instruction Categories
| Category | Cycles | Description |
|----------|--------|-------------|
| Stack Op | 1 | Push, pop, dup, swap, rot (pipelined) |
| ALU | 1 | Add, subtract, AND, OR, XOR on TOS (pipelined) |
| Memory | 3 | Fetch (@) and store (!) operations |
| Control | 2 | Branch, loop, conditional |
| Call/Return | 2 | Subroutine call and return |

## Stack Machine Architecture
- Two hardware stacks: data stack and return stack
- Top-of-stack (TOS) register for fast ALU access
- Next-on-stack (NOS) register
- Stack operations are zero-overhead (pipelined)
- Subroutine threading: CALL/RETURN in hardware

## Application
High-performance Forth execution:
- Real-time control systems
- Space applications (radiation-hardened)
- Embedded Forth systems
- Scientific instrument control

## Related Processors
- Novix NC4000 (predecessor concept)
- MuP21 (Chuck Moore's minimal design)
- ShBoom (later stack machine)
