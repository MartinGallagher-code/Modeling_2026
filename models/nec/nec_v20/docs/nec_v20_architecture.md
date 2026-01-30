# NEC V20 Architectural Documentation

## Era Classification

**Era:** Pipelined Execution
**Period:** 1984-1990
**Queueing Model:** Pipeline queueing network

## Architectural Features

- Pin-compatible 8088 replacement with enhanced microcode
- 10-20% faster than Intel 8088 at same clock speed
- Hardware multiply/divide (3-4x faster than 8088)
- 50% duty cycle (vs 33% on 8088)
- Dual internal 16-bit buses
- Improved effective address calculation
- 8080 emulation mode for legacy software
- Prefetch queue for instruction buffering
- 8-bit external data bus (8088-compatible)

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | NEC |
| Year | 1984 |
| Clock | 8.0 MHz |
| Transistors | 63,000 |
| Data Width | 16-bit |
| Address Width | 20-bit |

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
   - V20 achieves ~15% speedup over 8088 through improved microcode and hardware multiply/divide
   - Prefetch queue model with improved bus utilization (50% duty cycle vs 33%)
   - Hardware multiply reduces MUL from 118-133 cycles (8088) to ~29-30 cycles
   - Hardware divide similarly improved ~3x over 8088
   - Instruction categories: ALU (2c), data_transfer (3c), memory (4.5c), control (3c), multiply (4c weighted), divide (8c weighted)
   - Target CPI of 3.4 reflects ~15% improvement over 8088's CPI of 4.0

## Validation Approach

- Compare against original NEC datasheet timing specifications
- Cross-validate against Intel 8088 with documented 10-20% speedup factor
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/nec/v20)
- [Wikipedia](https://en.wikipedia.org/wiki/NEC_V20)

---
Generated: 2026-01-29
