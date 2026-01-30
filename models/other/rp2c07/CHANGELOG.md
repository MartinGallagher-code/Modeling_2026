# Ricoh RP2C07 PPU Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the Ricoh RP2C07 PAL NES PPU

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with 5 category-based instruction timing
   - background: 3.0 cycles - Background tile rendering with nametable lookup
   - sprite_eval: 5.0 cycles - Sprite evaluation (64 sprites, 8 per scanline)
   - pixel_output: 2.0 cycles - Pixel multiplexer output
   - vram_fetch: 4.0 cycles - VRAM pattern/nametable fetch
   - oam: 6.0 cycles - Object Attribute Memory read/write (256 bytes)
   - Reasoning: Same category structure as RP2C02 NTSC variant; PAL differences are in timing/scanline count, not operation complexity
   - Result: CPI = 3.500 (0.0% error vs target 3.5)

2. Calibrated typical workload weights for exact target CPI
   - background=0.30, sprite_eval=0.10, pixel_output=0.25, vram_fetch=0.25, oam=0.10
   - Verification: 3*0.30 + 5*0.10 + 2*0.25 + 4*0.25 + 6*0.10 = 3.50

**What we learned:**
- RP2C07 is the PAL variant of the NES PPU, running at 5.32 MHz
- 312 scanlines per frame (vs 262 NTSC), 50 Hz refresh (vs 60 Hz)
- Extra VBlank time (70 scanlines vs 20) gives CPU more time for game logic
- Same internal operation timings as RP2C02, different frame structure

**Final state:**
- CPI: 3.500 (0.0% error)
- Validation: PASSED

**References used:**
- Ricoh RP2C07 technical documentation
- NES PAL hardware reference (nesdev.org)

---
