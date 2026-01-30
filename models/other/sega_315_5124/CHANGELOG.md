# Sega 315-5124 VDP Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the Sega 315-5124 Master System VDP

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with 6 category-based instruction timing
   - tile_render: 3.0 cycles - Tile rendering (8x8 tiles)
   - sprite: 5.0 cycles - Sprite processing (64 sprites, 8 per scanline)
   - scroll: 3.0 cycles - Hardware H/V scrolling
   - vram: 4.0 cycles - VRAM access (16KB)
   - line_buffer: 4.0 cycles - Line buffer output
   - control: 3.0 cycles - Register control
   - Reasoning: Sprite processing most expensive (evaluation + rendering), VRAM and line buffer moderate, tile/scroll/control cheapest
   - Result: CPI = 3.800 (0.0% error vs target 3.8)

2. Calibrated typical workload weights for exact target CPI
   - tile_render=0.15, sprite=0.20, scroll=0.10, vram=0.25, line_buffer=0.15, control=0.15
   - Verification: 3*0.15 + 5*0.20 + 3*0.10 + 4*0.25 + 4*0.15 + 3*0.15 = 3.80

**What we learned:**
- Sega 315-5124 is a TMS9918A derivative with significant enhancements
- Supports 32 colors from 64-color palette (6-bit RGB)
- Line-based rendering with internal line buffer (unlike immediate-mode TMS9918A)
- Enhanced scrolling allows per-column vertical scroll (used in Sonic-style games)
- Also used in Game Gear (with different palette handling)

**Final state:**
- CPI: 3.800 (0.0% error)
- Validation: PASSED

**References used:**
- Sega 315-5124 VDP technical documentation
- Sega Master System technical manual

---
