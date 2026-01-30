# TI TMS34010 Architectural Documentation

## Era Classification

**Era:** Pipelined Execution
**Period:** 1980s Graphics Processor
**Queueing Model:** Pipeline queueing network

## Architectural Features

- First programmable graphics processor (GPU)
- 32-bit general-purpose instruction set plus dedicated pixel operations
- Hardware pixel processing with bit-level addressing
- Dedicated graphics pipeline operations (PIXBLT, LINE, FILL, DRAW)
- Used in arcade games (Mortal Kombat, NBA Jam) and early PC graphics cards
- Separate instruction and pixel processing paths
- On-chip frame buffer management

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Texas Instruments |
| Year | 1986 |
| Clock | 6.0 MHz |
| Transistors | 275,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |

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

Target CPI: 4.0 (graphics-focused workload)

Note: While the TMS34010 has a pipelined architecture, the high target CPI of 4.0 reflects the mix of fast ALU operations and slow multi-cycle graphics/pixel operations that dominate GPU workloads.

### Instruction Timing

| Category | Cycles | Description |
|----------|--------|-------------|
| ALU | 2 | ADD, SUB, AND, OR -- 32-bit general purpose |
| Data Transfer | 3 | MOV, register transfers |
| Memory | 4 | Load/store with bit-level addressing |
| Pixel | 5 | Pixel operations (PIXBLT, LINE) |
| Graphics | 6 | Graphics pipeline ops (FILL, DRAW) |
| Control | 5 | Branch, call, return |

## Model Implementation Notes

1. This processor uses the **Pipelined Execution** architectural template
2. Key modeling considerations:
   - The TMS34010 was the world's first programmable GPU, predating modern GPU architectures
   - Graphics operations (5-6 cycles) dominate typical workloads, driving CPI well above the ideal pipeline CPI of 1.0
   - Bit-level addressing capability adds complexity to memory operations (4 cycles)
   - General-purpose ALU operations are relatively fast (2 cycles) but represent only ~20% of typical workloads
   - Frame buffer access patterns create memory bottlenecks in graphics-heavy workloads
   - The 6 MHz clock was conservative but sufficient for 1986 arcade and PC graphics applications

## Validation Approach

- Compare against original Texas Instruments datasheet
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/ti/tms34010)
- [Wikipedia](https://en.wikipedia.org/wiki/TMS34010)

---
Generated: 2026-01-29
