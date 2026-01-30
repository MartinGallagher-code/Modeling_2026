# RCA CDP1861 Pixie Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1971-1976
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- DMA-based video display controller for COSMAC systems
- Generates 64x128 resolution video output
- Works alongside the RCA 1802 CPU via DMA transfers
- Used in CHIP-8 systems (Cosmac VIP)
- Simple display architecture: DMA fetch, active display, blanking, and sync phases
- No independent instruction execution -- operates as a display peripheral

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | RCA |
| Year | 1976 |
| Clock | 1.76 MHz |
| Transistors | 3,000 |
| Data Width | 8-bit |
| Address Width | 16-bit |

## Queueing Model Architecture

```
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│  FETCH  │──►│ DECODE  │──►│ EXECUTE │──►│ MEMORY  │
└─────────┘   └─────────┘   └─────────┘   └─────────┘
    │              │              │              │
    ▼              ▼              ▼              ▼
  M/M/1          M/M/1          M/M/1          M/M/1
  Queue          Queue          Queue          Queue

CPI = Fetch + Decode + Execute + Memory (serial sum)
```

## Operation Phase Timing Summary

| Category | Cycles | Description |
|----------|--------|-------------|
| DMA Fetch | 8 | DMA fetch from memory (6-10 cycles) |
| Display Active | 10 | Active display line rendering (8-12 cycles) |
| Blanking | 6 | Horizontal blanking interval (4-8 cycles) |
| Sync | 5 | Horizontal/vertical sync generation (4-6 cycles) |

**Note:** The CDP1861 is a video controller, not a general-purpose CPU. Its "instruction categories" represent display operation phases rather than traditional CPU instructions.

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - The CDP1861 is a display controller, not a standalone CPU
   - Operation phases model DMA-based video generation rather than instruction execution
   - Display active phase dominates the workload (~53% of time)
   - DMA fetch is a small fraction of overall operation (~2%)
   - Blanking and sync phases account for the remaining time
   - Clock frequency of 1.76 MHz is tied to NTSC video timing

## Validation Approach

- Compare against original RCA CDP1861 datasheet timing
- Validate display phase timing against NTSC video standards
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/rca/cosmac)
- [Wikipedia](https://en.wikipedia.org/wiki/CHIP-8)

---
Generated: 2026-01-29
