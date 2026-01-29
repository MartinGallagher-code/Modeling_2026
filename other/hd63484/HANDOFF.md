# Hitachi HD63484 ACRTC Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 1.3%
- **Last Updated**: 2026-01-29

## Current Model Summary

Architecture: 16-bit graphics command processor (1984)
Multi-cycle graphics commands with hardware acceleration.

| Category | Cycles | Description |
|----------|--------|-------------|
| draw_line | 6 | Line drawing command |
| draw_circle | 10 | Circle/arc drawing |
| area_fill | 8 | Area fill/paint |
| bitblt | 12 | Bit block transfer |
| char_display | 5 | Character display |
| control | 4 | Control/setup commands |
| dma | 3 | DMA/refresh operations |

**Performance:**
- Target CPI: 10.0
- Model CPI: 9.87
- At 8 MHz: ~800 KIPS

## Cross-Validation

Graphics command timing from HD63484 Technical Manual.
- Line: 6 cycles base
- Circle/Arc: 10 cycles base
- Area Fill: 8 cycles base
- BitBLT: 12 cycles base
- Actual execution time depends on drawing size (pixels affected)

## Known Issues

- Base cycle counts represent command setup overhead; actual per-pixel cost varies
- Model assumes typical drawing sizes for CPI weighting

## Suggested Next Steps

1. Model pixel-count-dependent execution time for more accuracy
2. Add display refresh DMA contention modeling

## Key Architectural Notes

- Advanced CRT Controller with built-in graphics engine
- 16-bit internal data path, 20-bit address bus
- Command FIFO for pipelined graphics operations
- Dual-port video RAM interface
- Used in Sharp X68000, arcade machines, CAD workstations

See CHANGELOG.md for full history of all work on this model.
