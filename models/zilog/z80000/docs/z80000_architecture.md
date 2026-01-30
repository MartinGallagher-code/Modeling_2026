# Zilog Z80000 Architectural Documentation

## Era Classification

**Era:** Pipelined Execution
**Period:** Mid 1980s (1986)
**Queueing Model:** Pipeline queueing network (sequential execution with instruction prefetch)

## Architectural Features

- 32-bit extension of the Z8000 architecture
- 32-bit data bus and 32-bit address bus (4 GB address space)
- 16 general-purpose 32-bit registers
- On-chip MMU with segmentation support
- Instruction prefetch buffer
- Up to 16 MHz clock
- ~91,000 transistors (CMOS)
- Microcoded complex instructions (3-80 cycles per instruction)
- Commercial failure with very limited adoption

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Zilog |
| Year | 1986 |
| Clock | 16.0 MHz |
| Transistors | 91,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |
| Registers | 16 x 32-bit general purpose |
| MMU | On-chip (segmented) |
| Target CPI | 6.0 |

## Queueing Model Architecture

```
┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐
│  IF  │─►│  ID  │─►│  OF  │─►│  EX  │─►│  WB  │
└──────┘  └──────┘  └──────┘  └──────┘  └──────┘
   │         │         │         │         │
   I1        I1        I1        I1        I1
             I2        I2        I2        I2

Ideal CPI = 1.0
Actual CPI = 1.0 + hazards + stalls + cache_misses
```

**Note:** The Z80000 uses instruction prefetch rather than a full pipeline, so actual CPI is significantly above 1.0. The pipeline diagram represents the conceptual execution stages.

## Instruction Categories

| Category | Cycles | Description |
|----------|--------|-------------|
| ALU (register) | 3 | ADD/SUB/AND/OR R,R |
| ALU (immediate) | 4 | ADD/SUB R,IM |
| Load | 5 | LD R,@RR (memory read) |
| Store | 5 | LD @RR,R (memory write) |
| Control | 6 | JP/JR (avg 5-7 cycles) |
| Call/Return | 10 | CALL @12, RET @8 (avg) |
| Multiply | 40 | MUL (35-45 cycles) |
| Divide | 55 | DIV (50-60 cycles) |

## Model Implementation Notes

1. This processor uses the **Pipelined Execution** architectural template (with instruction prefetch)
2. Key modeling considerations:
   - Extended Z8000 architecture to 32 bits with similar instruction set semantics
   - Instruction prefetch buffer provides limited overlap between fetch and execution stages
   - Microcoded multiply (40 cycles) and divide (55 cycles) are extremely slow relative to simple ALU ops (3 cycles)
   - The wide cycle range (3-55 cycles) means workload mix dramatically affects CPI
   - On-chip MMU with segmentation adds overhead for memory operations
   - Register-to-register ALU operations are fast at 3 cycles, benefiting from 32-bit datapath
   - Very limited documentation available due to commercial failure
   - Estimated timings are based on Z8000 heritage with 32-bit scaling
   - Typical workload CPI of 6.0 reflects the heavy microcode overhead for complex instructions

## Validation Approach

- Compare against available Zilog Z80000 documentation
- Cross-reference with Z8000 timing (scaled for 32-bit datapath)
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error
- Expected typical workload CPI: 6.0

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/zilog/z80000)
- [Wikipedia](https://en.wikipedia.org/wiki/Zilog_Z80000)

---
Generated: 2026-01-29
