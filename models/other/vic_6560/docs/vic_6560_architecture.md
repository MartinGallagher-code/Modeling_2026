# Commodore VIC (6560) Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1980
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Video Interface Chip for the Commodore VIC-20
- Character-based graphics rendering engine
- Simple sprite (movable object block) support
- Color attribute handling
- Display synchronization with CRT timing
- 8-bit data path with 14-bit address space (16KB)
- 1.02 MHz clock (NTSC version)
- Designed by MOS Technology / Commodore Semiconductor

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Commodore/MOS |
| Year | 1980 |
| Clock | 1.02 MHz |
| Transistors | ~5,000 |
| Data Width | 8-bit |
| Address Width | 14-bit |

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

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Video controller chip, not a general-purpose CPU
   - Character rendering is fastest operation at 3 cycles
   - Color attribute lookup averages 3.5 cycles
   - Sprite rendering and display sync average 5 cycles each
   - Bus sharing with CPU causes cycle stealing
   - Character mode is the primary rendering mode
   - Limited address space (14-bit = 16KB) constrains video memory

## Validation Approach

- Compare against original MOS/Commodore datasheet timing
- Validate with VIC-20 emulator cycle counts (VICE)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/mos_technology/6560)
- [Wikipedia](https://en.wikipedia.org/wiki/MOS_Technology_VIC)

---
Generated: 2026-01-29
