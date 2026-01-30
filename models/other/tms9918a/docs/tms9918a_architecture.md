# TI TMS9918A VDP Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1979
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Video Display Processor for TI-99/4A, MSX, ColecoVision, SG-1000
- Tile-based background rendering (8x8 tiles from pattern table)
- 32 hardware sprites with 4-per-scanline limit
- Hardware sprite collision detection
- 16KB VRAM via 14-bit address bus
- Multiple display modes: Graphics I/II, Multicolor, Text
- 8-bit data path to host CPU
- 10.7 MHz master clock
- Designed by Texas Instruments

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Texas Instruments |
| Year | 1979 |
| Clock | 10.7 MHz |
| Transistors | ~20,000 |
| Data Width | 8-bit |
| Address Width | 14-bit |

## Queueing Model Architecture

```
+----------+   +----------+   +----------+   +----------+   +----------+
|  SPRITE  |-->|  TILE    |-->|  VRAM    |-->|COLLISION |-->| CONTROL  |
|  ENGINE  |   |  RENDER  |   |  ACCESS  |   |  DETECT  |   |          |
+----------+   +----------+   +----------+   +----------+   +----------+
    |              |              |              |              |
    v              v              v              v              v
  M/M/1          M/M/1          M/M/1          M/M/1          M/M/1
  Queue          Queue          Queue          Queue          Queue

CPI = Weighted sum of category cycles
```

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Sprite engine is the most expensive operation at 6 cycles (evaluating 32 sprites)
   - Tile rendering involves pattern table lookup and attribute fetch
   - VRAM access is relatively fast at 3 cycles (dedicated VRAM bus)
   - Collision detection checks all sprite pairs in hardware
   - Control operations set registers and display modes
   - 5th sprite detection flag signals overflow condition

## Validation Approach

- Compare against TI TMS9918A datasheet timing specifications
- Validate with MSX/ColecoVision emulator cycle counts
- Target: <5% CPI prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/texas_instruments/tms9918)
- [Wikipedia](https://en.wikipedia.org/wiki/Texas_Instruments_TMS9918)

---
Generated: 2026-01-29
