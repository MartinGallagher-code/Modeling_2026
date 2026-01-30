# Hitachi HD63484 ACRTC Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Mid-1980s dedicated graphics processors
**Queueing Model:** Serial M/M/1 chain (command-driven graphics pipeline)

## Architectural Features

- Advanced CRT Controller (ACRTC) with built-in graphics engine
- 16-bit internal data path
- Hardware-accelerated line drawing, circle/arc generation, area fill, and BitBLT
- Multi-cycle graphics commands (variable execution time per command type)
- DMA for display refresh
- 20-bit address bus for 1 MB video memory address space
- Used in Sharp X68000, various arcade machines

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Hitachi |
| Year | 1984 |
| Clock | 8.0 MHz |
| Transistors | ~80,000 |
| Data Width | 16-bit |
| Address Width | 20-bit |

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

## Instruction Categories

| Category | Cycles | Description |
|----------|--------|-------------|
| Draw Line | 6 | Line drawing command |
| Draw Circle | 10 | Circle/arc drawing |
| Area Fill | 8 | Area fill/paint operation |
| BitBLT | 12 | Bit block transfer |
| Char Display | 5 | Character display |
| Control | 4 | Control/setup commands |
| DMA | 3 | DMA/refresh operations |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - The HD63484 is a graphics command processor, not a general-purpose CPU
   - CPI varies dramatically by command type (3 cycles for DMA to 12 cycles for BitBLT)
   - Typical graphics-heavy workloads are dominated by BitBLT operations (~52% weight)
   - Target CPI is ~10.0 for typical graphics workloads
   - The model uses command-level granularity rather than instruction-level
   - Actual pixel throughput depends on the number of pixels affected per command

## Validation Approach

- Compare against original Hitachi HD63484 datasheet command timings
- Validate with Sharp X68000 emulator measurements (if available)
- Cross-reference with arcade hardware timing documentation
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/hitachi/hd63484)
- [Wikipedia - HD63484](https://en.wikipedia.org/wiki/HD63484)

---
Generated: 2026-01-29
