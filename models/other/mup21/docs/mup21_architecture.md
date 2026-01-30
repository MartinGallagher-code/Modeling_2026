# MuP21 Architecture

## Overview
The MuP21 (1985) is an ultra-minimal Forth processor designed by Chuck Moore, featuring only ~7,000 transistors running at 50 MHz. It represents the extreme of minimalist processor design philosophy.

## Key Features
- 21-bit data bus and address bus
- 50 MHz clock frequency
- ~7,000 CMOS transistors
- Hardware data stack
- Hardware return stack
- Four 5-bit instructions per 20-bit word
- Integrated video output
- Single-cycle most operations

## Instruction Categories
| Category | Cycles | Description |
|----------|--------|-------------|
| Stack Op | 1 | Push, pop, dup, swap |
| ALU | 1 | Add, subtract, AND, OR, XOR, shift |
| Memory | 2 | Fetch and store operations |
| Control | 1 | Branch, call, return |
| I/O | 3 | I/O port and video operations |

## Instruction Packing
The MuP21 packs four 5-bit instructions into each 20-bit word:
- Slot 0: bits 19-15 (most operations)
- Slot 1: bits 14-10
- Slot 2: bits 9-5
- Slot 3: bits 4-0 (limited to jumps/calls)

This enables very high instruction throughput per memory access.

## Design Philosophy
Chuck Moore's minimalist approach:
- Fewer transistors = higher clock speed
- 21-bit word (not power-of-2) optimized for Forth
- Instruction packing maximizes throughput
- Hardware stacks eliminate memory overhead
- Integrated I/O reduces external chip count

## Application
Specialized Forth applications:
- Embedded control
- Video generation
- Real-time processing
- Research into minimal computing

## Related Processors
- Novix NC4000 (predecessor)
- F21 (successor by Chuck Moore)
- Harris RTX32P (commercial Forth processor)
