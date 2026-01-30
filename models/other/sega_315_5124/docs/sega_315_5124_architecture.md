# Sega 315-5124 VDP Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1985
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Sega Master System / Game Gear Video Display Processor
- TMS9918A derivative with significant enhancements
- Tile-based background rendering (8x8 tiles from VRAM)
- 64 hardware sprites, 8-per-scanline limit
- Hardware horizontal and vertical scrolling
- Per-column vertical scroll capability
- Line-based rendering with internal line buffer
- 32 colors from 64-color palette (6-bit RGB)
- 16KB VRAM via 14-bit address bus
- 10.7 MHz master clock
- Line interrupt counter for raster effects

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Sega |
| Year | 1985 |
| Clock | 10.7 MHz |
| Transistors | ~25,000 |
| Data Width | 8-bit |
| Address Width | 14-bit |

## Queueing Model Architecture

```
+----------+   +----------+   +----------+   +----------+   +----------+   +----------+
|  TILE    |-->|  SPRITE  |-->|  SCROLL  |-->|   VRAM   |-->|  LINE    |-->| CONTROL  |
|  RENDER  |   |          |   |          |   |  ACCESS  |   |  BUFFER  |   |          |
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
   - Tile rendering is fast at 3 cycles (pattern data already in VRAM)
   - Sprite processing is most expensive at 5 cycles (64 sprite evaluation)
   - Scrolling is lightweight at 3 cycles (hardware offset registers)
   - VRAM access takes 4 cycles (read/write with wait states)
   - Line buffer adds 4 cycles for scanline output compositing
   - Control register operations are fast at 3 cycles
   - Line interrupt counter enables per-scanline scroll changes

## Validation Approach

- Compare against Sega Master System technical documentation
- Validate with SMS emulator cycle-accurate timing (MEKA, Emulicious)
- Target: <5% CPI prediction error

## References

- [SMS Power! Technical Documentation](https://www.smspower.org/Development/VDPRegisters)
- [Wikipedia](https://en.wikipedia.org/wiki/Sega_Master_System)

---
Generated: 2026-01-29
