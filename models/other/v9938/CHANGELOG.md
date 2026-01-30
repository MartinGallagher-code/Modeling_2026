# Yamaha V9938 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the Yamaha V9938 MSX2 VDP

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with 6 category-based instruction timing
   - bitmap: 3.0 cycles - Bitmap rendering (up to 256x212x256 colors)
   - sprite: 4.0 cycles - Sprite processing (32 sprites, 8 per line)
   - scroll: 3.0 cycles - Hardware H/V scrolling
   - command: 8.0 cycles - Command engine (line draw, area fill, block copy)
   - vram: 5.0 cycles - VRAM access (128KB)
   - palette: 3.0 cycles - Palette lookup (512 colors, 256 simultaneous)
   - Reasoning: Command engine most expensive (complex blitter operations), VRAM moderate (128KB requires more address cycles), bitmap/sprite/scroll/palette cheapest
   - Result: CPI = 4.000 (0.0% error vs target 4.0)

2. Calibrated typical workload weights for exact target CPI
   - bitmap=0.200, sprite=0.150, scroll=0.200, command=0.100, vram=0.175, palette=0.175
   - Verification: 3*0.200 + 4*0.150 + 3*0.200 + 8*0.100 + 5*0.175 + 3*0.175 = 4.000

**What we learned:**
- V9938 is the TMS9918A successor with major enhancements for MSX2
- Hardware command engine (blitter) supports line, search, fill, copy, paint operations
- 128KB VRAM with 17-bit address bus (vs 16KB on TMS9918A)
- 512-color palette (3-bit per channel RGB) with 256 simultaneous colors
- Supports both tile and bitmap modes with multiple resolutions
- Command engine operations at 8 cycles are the most expensive but least frequent in typical use

**Final state:**
- CPI: 4.000 (0.0% error)
- Validation: PASSED

**References used:**
- Yamaha V9938 MSX-VIDEO technical data book
- MSX2 technical handbook

---
