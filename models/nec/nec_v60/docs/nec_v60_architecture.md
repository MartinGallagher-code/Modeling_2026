# NEC V60 Architectural Documentation

## Era Classification

**Era:** Pipelined Execution
**Period:** 1986-1992
**Queueing Model:** Pipeline queueing network

## Architectural Features

- Japan's first major 32-bit microprocessor
- New proprietary ISA (not x86 compatible)
- On-chip floating point unit
- String manipulation instructions
- 32-bit data and address bus (4GB address space)
- Used in NEC workstations and embedded systems
- Rich instruction set with FP and string support

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | NEC |
| Year | 1986 |
| Clock | 16.0 MHz |
| Transistors | 375,000 |
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
   - Proprietary NEC ISA, not x86 compatible (unlike V20/V30)
   - On-chip FPU adds floating point categories to instruction mix
   - String manipulation instructions are multi-cycle complex operations
   - Instruction categories: ALU (2c), data_transfer (2c), memory (4c), control (3c), float (8c), string (6c)
   - Target CPI of 3.0 reflects early 32-bit pipelined design
   - Stage timing: fetch (1c), decode (1c), execute (1c), memory (1c)

## Validation Approach

- Compare against original NEC datasheet timing specifications
- Cross-validate against contemporary 32-bit processors (MC68020, i386)
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/nec/v60)
- [Wikipedia](https://en.wikipedia.org/wiki/NEC_V60)

---
Generated: 2026-01-29
