# I860 Architectural Documentation

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
| Year | 1989 |
| Clock | 25.0 MHz |
| Transistors | 1,000,000 |
| Data Width | 64-bit |
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
   - Cache hierarchies with RISC-style execution

## Validation Approach

- Compare against original Intel datasheet
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/intel/i860)
- [Wikipedia](https://en.wikipedia.org/wiki/i860)

---
Generated: 2026-01-27
