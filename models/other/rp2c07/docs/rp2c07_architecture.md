# Ricoh RP2C07 PPU Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1986
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- PAL NES/Famicom Picture Processing Unit
- Same internal architecture as RP2C02 (NTSC) with PAL timing
- Background tile rendering with 2 nametables and scrolling
- 64 sprites stored in OAM (Object Attribute Memory, 256 bytes)
- 8-per-scanline sprite limit with priority and zero-hit detection
- 312 scanlines per frame at 50 Hz (vs 262 at 60 Hz NTSC)
- Extended VBlank period (70 scanlines vs 20)
- 5.32 MHz master clock (3x 1.77 MHz PAL CPU clock)

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Ricoh |
| Year | 1986 |
| Clock | 5.32 MHz |
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
   - Same internal operation timing as RP2C02 NTSC variant
   - PAL differences are in frame structure, not per-operation cycles
   - 312 scanlines: 240 visible + 72 blanking (more CPU time per frame)
   - 341 PPU cycles per scanline (same as NTSC)
   - Games designed for PAL have more VBlank time for CPU processing
   - Some NTSC games run slower on PAL due to 50 vs 60 Hz frame rate

## Validation Approach

- Compare against NES PPU timing documentation (nesdev.org)
- Validate with PAL NES emulator cycle-accurate timing
- Target: <5% CPI prediction error

## References

- [NESdev Wiki](https://www.nesdev.org/wiki/PPU)
- [Wikipedia](https://en.wikipedia.org/wiki/Picture_Processing_Unit)

---
Generated: 2026-01-29
