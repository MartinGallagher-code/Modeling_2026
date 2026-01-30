# NEC uPD7720 Architectural Documentation

## Era Classification

**Era:** Pipelined Execution
**Period:** 1980-1990
**Queueing Model:** Pipeline queueing network

## Architectural Features

- Early digital signal processor (DSP) for speech synthesis
- Hardware multiply-accumulate (MAC) unit with single-cycle throughput
- 16-bit data width, 13-bit instruction encoding
- Harvard architecture with separate program and data memory
- Pipelined execution optimized for real-time signal processing
- On-chip data RAM and program ROM
- NMOS technology
- Used in LPC vocoders and Super Nintendo APU (sound processor)

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | NEC |
| Year | 1980 |
| Clock | 8.0 MHz |
| Transistors | N/A |
| Data Width | 16-bit |
| Address Width | 13-bit |

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

## Model Implementation Notes

1. This processor uses the **Pipelined Execution** architectural template
2. Key modeling considerations:
   - DSP architecture optimized for single-cycle MAC operations
   - Instruction categories: MAC (1c), ALU (1c), memory (2c with 1c base + 1c memory), branch (2c due to pipeline flush)
   - Target CPI of 1.5 reflects efficient DSP pipeline with some branch and memory overhead
   - Harvard architecture enables simultaneous instruction and data fetch
   - Typical LPC vocoder workload: MAC 30%, ALU 20%, memory 30%, branch 20%
   - Compute-heavy workloads can achieve CPI closer to 1.0 (MAC-dominated)
   - Branch penalty is 2 cycles due to pipeline flush

## Validation Approach

- Compare against original NEC datasheet timing specifications
- Cross-validate with SNES APU performance characteristics
- Validate CPI range of 1.0-2.0 across all workloads
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/nec/upd7720)
- [Wikipedia](https://en.wikipedia.org/wiki/NEC_%C2%B5PD7720)

---
Generated: 2026-01-29
