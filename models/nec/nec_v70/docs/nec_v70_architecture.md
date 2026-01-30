# NEC V70 Architectural Documentation

## Era Classification

**Era:** Pipelined Execution
**Period:** 1987-1993
**Queueing Model:** Pipeline queueing network

## Architectural Features

- NEC V60 variant with higher clock speed and improved pipeline
- Same proprietary ISA as V60 (not x86 compatible)
- On-chip floating point unit
- String manipulation instructions
- 32-bit data and address bus (4GB address space)
- Slightly improved pipeline efficiency over V60
- Used in NEC workstations

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | NEC |
| Year | 1987 |
| Clock | 20.0 MHz |
| Transistors | 400,000 |
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
   - Same ISA as V60 but with improved pipeline and higher clock
   - Slightly lower CPI than V60 due to pipeline improvements
   - Instruction categories: ALU (2c), data_transfer (2c), memory (3.5c), control (3c), float (7c), string (5.5c)
   - Target CPI of 2.8 reflects pipeline improvements over V60's CPI of 3.0
   - Memory operations slightly faster (3.5c vs 4c) due to improved bus interface
   - Float and string operations also slightly improved over V60

## Validation Approach

- Compare against original NEC datasheet timing specifications
- Cross-validate against V60 model (V70 should be ~7% faster per-clock)
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/nec/v70)
- [Wikipedia](https://en.wikipedia.org/wiki/NEC_V70)

---
Generated: 2026-01-29
