# NEC V30 Architectural Documentation

## Era Classification

**Era:** Pipelined Execution
**Period:** 1984-1990
**Queueing Model:** Pipeline queueing network

## Architectural Features

- Pin-compatible 8086 replacement with enhanced microcode
- 16-bit external data bus (vs V20's 8-bit)
- ~30% faster than Intel 8086 at same clock speed
- Hardware multiply/divide (3-4x faster than 8086)
- 50% duty cycle (vs 33% on 8086)
- Dual internal 16-bit buses
- Improved effective address calculation
- 8080 emulation mode for legacy software
- Prefetch queue with wider bus bandwidth

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | NEC |
| Year | 1984 |
| Clock | 10.0 MHz |
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
   - V30 is the 16-bit bus sibling of V20 (V20 is 8088-compatible, V30 is 8086-compatible)
   - 16-bit external bus provides faster memory access than V20's 8-bit bus
   - ~30% speedup over 8086 through improved microcode, hardware multiply/divide, and bus efficiency
   - Hardware multiply reduces MUL from 118-128 cycles (8086) to ~27-28 cycles
   - Instruction categories: ALU (2c), data_transfer (2.5c), memory (4c), control (2.5c), multiply (4c weighted), divide (7c weighted)
   - Target CPI of 3.2 reflects ~30% improvement over 8086's CPI of 4.5

## Validation Approach

- Compare against original NEC datasheet timing specifications
- Cross-validate against Intel 8086 with documented ~30% speedup factor
- Cross-validate against V20 model (V30 should be faster for memory workloads)
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/nec/v30)
- [Wikipedia](https://en.wikipedia.org/wiki/NEC_V30)

---
Generated: 2026-01-29
