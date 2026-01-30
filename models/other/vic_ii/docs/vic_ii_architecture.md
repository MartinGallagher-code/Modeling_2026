# Commodore VIC-II (6567) Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1982
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Commodore 64 Video Interface Controller (6567 NTSC / 6569 PAL)
- Character and bitmap graphics modes (text, hires, multicolor)
- 8 hardware sprites with multicolor and 2x expansion
- Hardware smooth scrolling (horizontal and vertical, 3-bit fine scroll)
- Raster interrupt generation for split-screen effects
- DMA cycle stealing from 6510 CPU bus ("badlines")
- 12-bit multiplexed data bus for 16KB video RAM access
- 16 fixed colors (no palette programming)
- 8 MHz master clock (NTSC 6567)

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | MOS Technology/Commodore |
| Year | 1982 |
| Clock | 8 MHz |
| Transistors | ~16,000 |
| Data Width | 12-bit |
| Address Width | 14-bit |

## Queueing Model Architecture

```
+----------+   +----------+   +----------+   +----------+   +----------+   +----------+
| CHAR_GEN |-->|  SPRITE  |-->|  SCROLL  |-->|  RASTER  |-->|   DMA    |-->|  COLOR   |
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
   - Character generation is the most frequent operation in text mode
   - 8 sprites with per-sprite enable, multicolor, and expansion flags
   - Smooth scrolling requires extra fetch cycles for border handling
   - Raster interrupts are essential for advanced effects (demo scene)
   - DMA "badlines" steal 40-43 CPU cycles per character row (every 8 lines)
   - Color RAM is separate 4-bit memory (1000 nybbles)
   - 12-bit bus multiplexes address and data for video memory access

## Validation Approach

- Compare against MOS 6567/6569 datasheet timing
- Validate with VICE emulator cycle-accurate timing
- Target: <5% CPI prediction error

## References

- [C64 Wiki - VIC-II](https://www.c64-wiki.com/wiki/VIC)
- [Wikipedia](https://en.wikipedia.org/wiki/MOS_Technology_VIC-II)

---
Generated: 2026-01-29
