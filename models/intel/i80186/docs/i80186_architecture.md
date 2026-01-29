# I80186 Architectural Documentation

## Era Classification

**Era:** Prefetch Queue  
**Period:** 1976-1982  
**Queueing Model:** Parallel M/M/1 queues with synchronization

## Architectural Features

- Instruction prefetch queue (4-6 bytes)
- BIU fetches while EU executes
- Queue can stall on branches/jumps
- Bus contention between fetch and memory ops
- Some instruction overlap possible

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Intel |
| Year | 1982 |
| Clock | 6.0 MHz |
| Transistors | 55,000 |
| Data Width | 16-bit |
| Address Width | 20-bit |

## Queueing Model Architecture


```
┌─────────────────────────────────────────┐
│              Bus Interface Unit (BIU)    │
│  ┌──────────┐    ┌──────────────────┐  │
│  │  Memory  │───►│  Prefetch Queue  │  │
│  │  Access  │    │  (4-6 bytes)     │  │
│  └──────────┘    └────────┬─────────┘  │
└───────────────────────────┼────────────┘
                            │
                            ▼
┌─────────────────────────────────────────┐
│            Execution Unit (EU)           │
│  ┌──────────┐    ┌──────────────────┐  │
│  │  Decode  │───►│     Execute      │  │
│  └──────────┘    └──────────────────┘  │
└─────────────────────────────────────────┘

BIU and EU operate in PARALLEL
CPI = max(BIU_time, EU_time) + contention + stalls
```

## Model Implementation Notes

1. This processor uses the **Prefetch Queue** architectural template
2. Key modeling considerations:
   - Parallel Bus Interface Unit (BIU) and Execution Unit (EU)

## Validation Approach

- Compare against original Intel datasheet
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/intel/i80186)
- [Wikipedia](https://en.wikipedia.org/wiki/i80186)

---
Generated: 2026-01-27
