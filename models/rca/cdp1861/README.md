# RCA CDP1861 (Pixie)

## Quick Reference
| Parameter | Value |
|-----------|-------|
| Year | 1976 |
| Type | Video Display Controller |
| Clock | 1.7609 MHz (NTSC) |
| Transistors | ~2,000 (est.) |
| Process | CMOS |
| Display | 64x32 pixels |
| Standard | NTSC (60 Hz) |
| Companion | CDP1802 COSMAC CPU |

## Description
The CDP1861 "Pixie" is a video display controller designed to work with the
RCA CDP1802 COSMAC CPU. It is NOT a general-purpose processor. It generates
a 64x32 pixel monochrome display by stealing DMA cycles from the 1802 CPU
during active display periods.

Used in CHIP-8 systems and early hobbyist computers (COSMAC VIP, Studio II).
During active display, the 1861 requests DMA from the 1802 to fetch 8 bytes
per scanline (8 bytes x 8 bits = 64 pixels). This cycle-stealing reduces
available CPU time during video output.

## Validation Status
- **Status**: PASSED
- **CPI Error**: 2.9%
- **Model CPI**: 8.229 (target: 8.0)
- **Last Validated**: 2026-01-29

## Operation Categories
| Category | Cycles | Description |
|----------|--------|-------------|
| DMA Fetch | 2 | Steal 2 cycles from 1802 per byte |
| Display Active | 4 | Shift out pixel data |
| Horizontal Blank | 6 | H-blank interval |
| Vertical Blank | 17 | V-blank lines (no DMA) |
| Sync | 10 | H-sync and V-sync |
| Interrupt | 16 | End-of-frame interrupt |

## Notes
CPI metric represents average cycles per video state machine operation,
not traditional instruction execution. The primary bottleneck is the
sync generator timing.
