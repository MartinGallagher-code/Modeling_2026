# Inmos T800 Architectural Documentation

## Era Classification

**Era:** Pipelined Execution
**Period:** Late 1980s (1987)
**Queueing Model:** Pipeline queueing network

## Architectural Features

- 32-bit transputer with on-chip IEEE 754 floating-point unit
- CSP (Communicating Sequential Processes) concurrency model
- 4KB on-chip SRAM
- Designed for Occam programming language
- Hardware process scheduler with lightweight context switching
- Four serial communication links for inter-transputer networking
- Pipelined integer and floating-point execution
- 20 MHz clock (fastest transputer of its era)
- 250,000 transistors
- Used in parallel supercomputers and signal processing

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Inmos |
| Year | 1987 |
| Clock | 20.0 MHz |
| Transistors | 250,000 |
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

## Model Implementation Notes

1. This processor uses the **Pipelined Execution** architectural template
2. Key modeling considerations:
   - Integer ALU operations average 1.5 cycles (near single-cycle pipelining)
   - On-chip FPU provides fast floating-point (2.5 cycles avg)
   - Memory operations benefit from 4KB on-chip SRAM (2.5 cycles)
   - Control/process scheduling averages 3 cycles
   - Channel communication operations average 3.5 cycles
   - Dominant ALU-heavy workload mix (62.5% ALU in typical profile)
   - On-chip FPU was a major differentiator over T414/T424
   - Pipelined execution enables overlapped integer and FP operations

## Validation Approach

- Compare against original Inmos T800 datasheet timing
- Validate with transputer emulator cycle counts
- Cross-validate with T212 and T424 transputer family
- Compare FLOPS against published T800 benchmarks
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/inmos/t800)
- [Wikipedia](https://en.wikipedia.org/wiki/Transputer)

---
Generated: 2026-01-29
