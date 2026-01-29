# I80387 Architectural Documentation

## Era Classification

**Era:** Cache/RISC Architecture  
**Period:** 1983-1988  
**Queueing Model:** Cache hierarchy + pipeline network

## Architectural Features

- On-chip instruction cache
- Deep pipeline (5+ stages)
- Load/store architecture
- Register windows or large register files
- Single-cycle execution goal
- Delayed branches

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Intel |
| Year | Unknown |
| Clock | Unknown MHz |
| Transistors | Unknown |
| Data Width | 8-bit |
| Address Width | 16-bit |

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
   - Cache hierarchies with RISC-style execution

## Validation Approach

- Compare against original manufacturer datasheet
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/intel/i80387)
- [Wikipedia](https://en.wikipedia.org/wiki/i80387)

---
Generated: 2026-01-27
