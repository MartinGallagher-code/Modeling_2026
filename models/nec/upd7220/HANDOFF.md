# NEC uPD7220 Graphics Display Controller Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: <5%
- **Last Updated**: 2026-01-29
- **Cross-validation**: Initial validation complete

## Current Model Summary
- Architecture: 16-bit graphics command processor (NOT a general CPU)
- Clock: 5.0 MHz
- Target CPI: 12.0 (per graphics command)
- Predicted CPI: 11.99

Key instruction categories:
| Category | Cycles | Description |
|----------|--------|-------------|
| draw_line | 16 | Line drawing (Bresenham) per pixel step |
| draw_arc | 24 | Arc drawing per step |
| area_fill | 14 | Area fill command |
| char_display | 8 | Character display from font |
| dma_transfer | 4 | DMA transfer per word |
| control | 3 | Control/status commands |

## Cross-Validation Summary
- Per-instruction tests: Initial validation
- Reference sources: NEC uPD7220 GDC Technical Manual

## Known Issues
- None - model validated within 5% error
- Note: CPI metric represents average cycles per graphics command, not traditional CPU instructions

## Suggested Next Steps
- Could add scroll/pan command timing
- Consider modeling display memory bandwidth constraints

## Key Architectural Notes
- NEC uPD7220 (1981) - first single-chip LSI graphics display controller
- NOT a general-purpose CPU - specialized graphics command processor
- ~60000 transistors, 16-bit internal data path
- Hardware Bresenham line drawing, arc generation, area fill
- DMA to display memory, video timing generation
- Used in NEC PC-9801 and IBM Professional Graphics Controller
- 20-bit address bus for up to 1MB display memory
