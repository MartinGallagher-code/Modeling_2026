# Commodore TED (7360) Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1984
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Commodore C16/Plus/4 integrated video, sound, and timer controller
- Character and bitmap graphics modes (no hardware sprites)
- 121-color palette (16 hues x 8 luminance levels, minus duplicates)
- 2-channel square wave sound generator
- 3 programmable 16-bit timers
- DMA cycle stealing for video refresh
- Replaces VIC-II + SID + CIA in a single chip
- 8-bit data bus, 16-bit address space
- 7 MHz master clock

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | MOS Technology/Commodore |
| Year | 1984 |
| Clock | 7 MHz |
| Transistors | ~25,000 |
| Data Width | 8-bit |
| Address Width | 16-bit |

## Queueing Model Architecture

```
+----------+   +----------+   +----------+   +----------+   +----------+   +----------+
| CHAR_GEN |-->|  COLOR   |-->|  SOUND   |-->|  TIMER   |-->|   DMA    |-->| CONTROL  |
+----------+   +----------+   +----------+   +----------+   +----------+   +----------+
    |              |              |              |              |              |
    v              v              v              v              v              v
  M/M/1          M/M/1          M/M/1          M/M/1          M/M/1          M/M/1
  Queue          Queue          Queue          Queue          Queue          Queue

CPI = Weighted sum of category cycles
```

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Character generation dominates the workload (25% weight)
   - 121-color palette requires luminance+chrominance lookup (4 cycles)
   - Sound generation is simpler than SID (2 square channels only)
   - Timer management includes 3 independent 16-bit countdown timers
   - DMA cycle stealing is the most expensive operation (bus arbitration)
   - No sprites means all moving objects require software rendering
   - Integration reduces chip count but limits individual subsystem capability

## Validation Approach

- Compare against MOS 7360 TED datasheet timing
- Validate with Plus/4 emulator timing data
- Target: <5% CPI prediction error

## References

- [Plus/4 Wiki](https://plus4world.powweb.com/)
- [Wikipedia](https://en.wikipedia.org/wiki/MOS_Technology_TED)

---
Generated: 2026-01-29
