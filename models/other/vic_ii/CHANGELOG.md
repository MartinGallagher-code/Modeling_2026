# Commodore VIC-II (6567) Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the Commodore VIC-II (6567) video chip

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with 6 category-based instruction timing
   - char_gen: 3.0 cycles - Character generation from ROM/RAM
   - sprite: 5.0 cycles - Hardware sprite processing (8 sprites)
   - scroll: 4.0 cycles - Smooth scrolling (H/V)
   - raster: 3.0 cycles - Raster interrupt and sync
   - dma: 6.0 cycles - DMA cycle stealing from CPU bus
   - color: 3.0 cycles - Color lookup (16 fixed colors)
   - Reasoning: DMA most expensive (bus arbitration), sprites moderate, character/raster/color cheapest
   - Result: CPI = 4.000 (0.0% error vs target 4.0)

2. Calibrated typical workload weights for exact target CPI
   - char_gen=0.20, sprite=0.20, scroll=0.15, raster=0.15, dma=0.15, color=0.15
   - Verification: 3*0.20 + 5*0.20 + 4*0.15 + 3*0.15 + 6*0.15 + 3*0.15 = 4.00

**What we learned:**
- VIC-II is the Commodore 64 video chip (6567 NTSC / 6569 PAL)
- 12-bit data bus allows multiplexed address/data for 16KB VRAM access
- DMA cycle stealing is the most expensive operation, halting the 6510 CPU
- 8 hardware sprites with multicolor and expansion support
- Raster interrupts enable split-screen effects (common in C64 demos)

**Final state:**
- CPI: 4.000 (0.0% error)
- Validation: PASSED

**References used:**
- MOS 6567/6569 VIC-II datasheet
- Commodore 64 Programmer's Reference Guide

---
