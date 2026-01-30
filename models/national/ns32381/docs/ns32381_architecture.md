# National NS32381 Architectural Documentation

## Era Classification

**Era:** Pipelined Execution
**Period:** Mid-1980s 32-bit floating-point coprocessors
**Queueing Model:** Pipeline queueing network

## Architectural Features

- Second-generation floating-point coprocessor for the NS32000 family
- Pipelined execution for improved throughput over NS32081
- IEEE 754 compatible floating-point standard support
- 32-bit data path with full single and double precision support
- Higher clock speed (15 MHz vs 10 MHz for NS32081)
- Improved floating-point add, multiply, and divide performance
- Tightly coupled with NS32332 and other NS32000 series processors
- 60,000 transistors enabling pipelined datapath

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | National Semiconductor |
| Year | 1985 |
| Clock | 15.0 MHz |
| Transistors | 60,000 |
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

### Instruction Category Timing

| Category | Cycles | Description |
|----------|--------|-------------|
| FP Add | 6.0 | Floating-point add/subtract (5-7 cycles) |
| FP Multiply | 8.0 | Floating-point multiply (7-9 cycles) |
| FP Divide | 16.0 | Floating-point divide (12-20 cycles) |
| Data Transfer | 4.0 | Register/memory transfers (3-5 cycles) |

## Model Implementation Notes

1. This processor uses the **Pipelined Execution** architectural template
2. Key modeling considerations:
   - Significantly faster than NS32081 due to pipelining and higher clock (15 MHz vs 10 MHz)
   - FP add reduced from 8 to 6 cycles; FP multiply from 12 to 8 cycles
   - FP divide reduced from 20 to 16 cycles through improved iterative algorithm
   - Data transfer at 4 cycles reflects improved bus interface
   - 60,000 transistors (vs NS32081) enable the pipelined datapath
   - As a coprocessor, fetch is handled by the host processor
   - Multiply operations dominate typical workloads (~47% weight)

## Validation Approach

- Compare against original National Semiconductor NS32381 datasheet timing tables
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/national_semiconductor/ns32381)
- [Wikipedia](https://en.wikipedia.org/wiki/NS32000)

---
Generated: 2026-01-29
