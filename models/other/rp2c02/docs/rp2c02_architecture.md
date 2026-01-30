# Ricoh RP2C02 PPU Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1983
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- NES/Famicom Picture Processing Unit (NTSC variant)
- Background tile rendering with 2 nametables and scrolling
- 64 sprites stored in OAM (Object Attribute Memory, 256 bytes)
- 8-per-scanline sprite limit with priority and zero-hit detection
- 2 pattern tables (4KB each) for tile/sprite graphics
- Pixel output multiplexer for background/sprite priority
- 14-bit VRAM address bus (16KB addressable)
- 5.37 MHz master clock (3x CPU clock)
- 262 scanlines, 341 cycles per scanline, 60 Hz NTSC

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Ricoh |
| Year | 1983 |
| Clock | 5.37 MHz |
| Transistors | ~16,000 |
| Data Width | 8-bit |
| Address Width | 14-bit |

## Queueing Model Architecture

```
+----------+   +----------+   +----------+   +----------+   +----------+
|BACKGROUND|-->|  SPRITE  |-->|  PIXEL   |-->|  VRAM    |-->|   OAM    |
|  RENDER  |   |   EVAL   |   |  OUTPUT  |   |  FETCH   |   |          |
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
   - Background rendering is the most frequent operation (every visible pixel)
   - Sprite evaluation happens during specific scanline phases (cycles 257-320)
   - Pixel output is the simplest operation (priority mux between BG and sprites)
   - VRAM fetches interleave nametable, attribute, and pattern data
   - OAM operations are most expensive due to secondary OAM evaluation
   - Rendering is disabled during VBlank (scanlines 241-261)

## Validation Approach

- Compare against NES PPU timing documentation (nesdev.org)
- Validate with NES emulator cycle-accurate timing
- Target: <5% CPI prediction error

## References

- [NESdev Wiki](https://www.nesdev.org/wiki/PPU)
- [Wikipedia](https://en.wikipedia.org/wiki/Picture_Processing_Unit)

---
Generated: 2026-01-29
