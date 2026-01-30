# Berkeley RISC I Architectural Documentation

## Era Classification

**Era:** Cache/RISC Architecture
**Period:** Early 1980s (1982)
**Queueing Model:** Cache hierarchy + pipeline network

## Architectural Features

- First RISC processor (UC Berkeley, David Patterson)
- 2-stage pipeline (fetch/decode + execute)
- 78 registers with 6 overlapping register windows
- Delayed branches with 1 branch delay slot
- Load/store architecture -- only loads/stores access memory
- 31 instructions total (reduced instruction set)
- Single-cycle ALU operations
- Precursor to Sun SPARC architecture

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | UC Berkeley |
| Year | 1982 |
| Clock | 4.0 MHz |
| Transistors | 44,500 |
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
   - Target CPI of 1.3 reflects near single-cycle execution
   - ALU operations execute in 1 cycle (true RISC design)
   - Load/store operations take 2 cycles due to memory access
   - Branch delay slots allow branches at 1 cycle when filled
   - Register windows eliminate most procedure call overhead (CALL = 1 cycle)
   - 40% ALU, 20% load, 10% store, 20% branch, 10% call in typical workload
   - CPI much lower than contemporary CISC designs (VAX CPI ~10)

## Validation Approach

- Compare against original UC Berkeley RISC I papers
- Validate CPI < 2.0 (RISC principle)
- Verify >5x speedup over VAX 11/780 (CPI ~10)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/berkeley/risc_i)
- [Wikipedia](https://en.wikipedia.org/wiki/Berkeley_RISC)

---
Generated: 2026-01-29
