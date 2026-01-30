# Yamaha V9938 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1985
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- MSX2 Video Display Processor (TMS9918A successor)
- Bitmap modes up to 256x212 in 256 colors
- Tile-based and character modes (backward compatible with TMS9918A)
- 32 hardware sprites, 8 per scanline, 16x16 support
- Hardware horizontal and vertical scrolling
- Hardware command engine (blitter) for 2D operations
- Command set: LINE, SRCH, PSET, POINT, HMMC, YMMM, HMMM, HMMV, LMMC, LMCM, LMMM, LMMV
- 128KB VRAM via 17-bit address bus
- 512-color palette (3 bits per RGB channel), 256 simultaneous
- 21.5 MHz master clock
- ~60,000 transistors

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Yamaha |
| Year | 1985 |
| Clock | 21.5 MHz |
| Transistors | ~60,000 |
| Data Width | 8-bit |
| Address Width | 17-bit |

## Queueing Model Architecture

```
+----------+   +----------+   +----------+   +----------+   +----------+   +----------+
|  BITMAP  |-->|  SPRITE  |-->|  SCROLL  |-->| COMMAND  |-->|   VRAM   |-->| PALETTE  |
|  RENDER  |   |          |   |          |   |  ENGINE  |   |  ACCESS  |   |          |
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
   - Bitmap rendering is fast at 3 cycles (direct pixel addressing)
   - Sprite processing takes 4 cycles (32 sprites with color/size options)
   - Scrolling is lightweight at 3 cycles (hardware offset registers)
   - Command engine is most expensive at 8 cycles (complex blitter operations)
   - VRAM access takes 5 cycles (128KB with longer address setup)
   - Palette lookup is fast at 3 cycles (256-entry LUT)
   - Command engine can operate asynchronously while CPU continues
   - Backward compatible with TMS9918A modes

## Validation Approach

- Compare against Yamaha V9938 MSX-VIDEO technical data book
- Validate with MSX2 emulator timing data (openMSX)
- Target: <5% CPI prediction error

## References

- [MSX Wiki - V9938](https://www.msx.org/wiki/Yamaha_V9938)
- [Wikipedia](https://en.wikipedia.org/wiki/Yamaha_V9938)

---
Generated: 2026-01-29
