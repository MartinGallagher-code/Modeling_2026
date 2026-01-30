# Novix NC4000 Architecture

## Overview
The Novix NC4000 (1983) is the first single-chip Forth processor, designed by Chuck Moore (the inventor of Forth). It executes Forth primitives directly in hardware with minimal transistor count.

## Key Features
- 16-bit data bus and address bus
- 8 MHz clock frequency
- ~16,000 CMOS transistors
- Hardware data stack (256 deep)
- Hardware return stack (256 deep)
- Single-cycle Forth primitives
- Subroutine threaded code in hardware
- Instruction packing (multiple ops per word)

## Instruction Categories
| Category | Cycles | Description |
|----------|--------|-------------|
| Stack Op | 1 | Push, pop, dup, swap, over, rot |
| ALU | 1 | Add, subtract, AND, OR, XOR on TOS |
| Memory | 3 | Fetch (@) and store (!) operations |
| Control | 2 | Branch, loop, IF/THEN |
| Call/Return | 1 | Hardware subroutine threading |

## Stack Machine Architecture
- Two hardware stacks: data and return
- Top-of-stack (TOS) in dedicated register
- Subroutine threading: Forth words are called directly
- No instruction decode overhead for stack operations
- Instruction packing allows multiple primitives per 16-bit word

## Application
Direct Forth execution:
- Embedded real-time control
- Scientific computing
- AI/expert systems
- Rapid prototyping

## Related Processors
- Harris RTX2000/RTX32P (commercial successors)
- MuP21 (Chuck Moore's later minimal design)
- F21 (further evolution by Moore)
