# Berkeley RISC II Architectural Documentation

## Era Classification

**Era:** Cache/RISC Architecture
**Period:** Early 1980s (1983)
**Queueing Model:** Cache hierarchy + pipeline network

## Architectural Features

- Improved second RISC processor from UC Berkeley
- 3-stage pipeline (fetch, decode, execute)
- 138 registers with 8 overlapping register windows (32 registers per window)
- Single-cycle ALU operations
- Load/store architecture with delayed branches
- 39 instructions (expanded from RISC I's 31)
- Write buffer for store operations (1.5 cycles vs 2 for loads)
- Direct influence on Sun SPARC architecture
- Fewer transistors than RISC I but more efficient

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | UC Berkeley |
| Year | 1983 |
| Clock | 3.0 MHz |
| Transistors | 40,760 |
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
   - Target CPI of 1.2 (improved over RISC I's 1.3)
   - ALU operations: 1 cycle (single-cycle RISC design)
   - Load operations: 2 cycles (memory access latency)
   - Store operations: 1.5 cycles (write buffer optimization)
   - Branch: 2 cycles (with delay slot)
   - CALL/RET: 1 cycle (register window switch, zero-overhead)
   - 8 register windows (vs RISC I's 6) reduce memory traffic
   - High ALU percentage (62%) in typical workload reflects RISC philosophy
   - >5% CPI improvement over RISC I validated

## Validation Approach

- Compare against original UC Berkeley RISC II papers
- Validate CPI < 1.5 (improved RISC)
- Verify improvement over RISC I (>5%)
- Verify >6x speedup over VAX 11/780
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/berkeley/risc_ii)
- [Wikipedia](https://en.wikipedia.org/wiki/Berkeley_RISC)

---
Generated: 2026-01-29
