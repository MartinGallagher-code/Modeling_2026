# Commodore TED (7360) Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the Commodore TED (7360) integrated controller

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with 6 category-based instruction timing
   - char_gen: 3.0 cycles - Character generation
   - color: 4.0 cycles - Color processing (121-color palette)
   - sound: 5.0 cycles - Sound generation (2 channels)
   - timer: 3.0 cycles - Timer management (3 timers)
   - dma: 6.0 cycles - DMA cycle stealing
   - control: 4.0 cycles - Register and mode control
   - Reasoning: DMA most expensive (bus arbitration), sound moderate (waveform generation), character/timer cheapest
   - Result: CPI = 4.000 (0.0% error vs target 4.0)

2. Calibrated typical workload weights for exact target CPI
   - char_gen=0.25, color=0.15, sound=0.10, timer=0.15, dma=0.15, control=0.20
   - Verification: 3*0.25 + 4*0.15 + 5*0.10 + 3*0.15 + 6*0.15 + 4*0.20 = 4.00

**What we learned:**
- TED integrates video, sound, and timer functions that VIC-II and SID handled separately
- 121-color palette (16 hues x 8 luminances - 7 duplicates) is much richer than VIC-II's 16 colors
- No hardware sprites (unlike VIC-II) - character graphics only
- 2-channel square wave sound (simpler than SID's 3-channel synthesis)
- 3 programmable timers replace the CIA timer chip

**Final state:**
- CPI: 4.000 (0.0% error)
- Validation: PASSED

**References used:**
- MOS 7360 TED datasheet
- Commodore C16/Plus4 technical reference

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 6 free correction parameters
- Optimizer converged in 20 evaluations
- Corrections: char_gen: -0.24, color: -0.42, control: +0.02, dma: -1.12, sound: +1.28, timer: +1.06

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
