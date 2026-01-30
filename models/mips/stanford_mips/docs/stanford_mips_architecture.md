# Stanford MIPS Architectural Documentation

## Era Classification

**Era:** Cache/RISC Architecture
**Period:** Early 1980s (1983)
**Queueing Model:** Cache hierarchy + pipeline network

## Architectural Features

- Original MIPS (Microprocessor without Interlocked Pipeline Stages) from Stanford
- 5-stage pipeline: IF, ID, EX, MEM, WB
- 32-bit RISC load/store architecture
- 32 general-purpose registers
- Delayed branches with 1 delay slot
- Software-scheduled load delay slots
- Hardwired control (no microcode)
- Interlocked pipeline for hazard handling
- Designed by John Hennessy's research group
- Precursor to commercial MIPS R2000 (1986)

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Stanford University |
| Year | 1983 |
| Clock | 2.0 MHz |
| Transistors | ~25,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |

## Queueing Model Architecture

```
                    ┌────────────┐
                    │  I-Cache   │
                    └─────┬──────┘
                          │
┌──────┐  ┌──────┐  ┌─────▼────┐  ┌──────┐  ┌──────┐
│  IF  │─►│  ID  │─►│    EX    │─►│  MEM │─►│  WB  │
└──────┘  └──────┘  └──────────┘  └──┬───┘  └──────┘
                                     │
                               ┌─────▼──────┐
                               │  D-Cache   │
                               └────────────┘

RISC Goal: CPI ≈ 1.0
Actual CPI = 1.0 + cache_misses + hazards + branch_penalties
```

## Model Implementation Notes

1. This processor uses the **Cache/RISC Architecture** architectural template
2. Key modeling considerations:
   - 5-stage pipeline achieves near single-cycle execution for ALU ops
   - ALU, store, and jump operations execute in 1 cycle (ideal pipelining)
   - Load operations average 1.5 cycles due to load delay slot penalties
   - Branch operations average 1.5 cycles due to delayed branch overhead
   - Target CPI: ~1.2 (accounting for realistic hazards)
   - Software scheduling of delay slots is key to performance
   - Compared favorably to Berkeley RISC I (CPI ~1.3) and RISC II (CPI ~1.2)
   - Represents 6-8x speedup over VAX 11/780 (CPI ~10)

## Validation Approach

- Compare against Stanford MIPS research papers (Hennessy et al.)
- Cross-validate with Berkeley RISC I/II performance data
- Validate CPI < 1.5 (RISC single-cycle goal)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/stanford/mips)
- [Wikipedia](https://en.wikipedia.org/wiki/MIPS_architecture)

---
Generated: 2026-01-29
