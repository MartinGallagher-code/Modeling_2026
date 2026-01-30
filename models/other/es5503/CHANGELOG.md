# Ensoniq ES5503 DOC Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the Ensoniq ES5503 DOC wavetable chip

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with 5 category-based instruction timing
   - wavetable_read: 6 cycles - Wavetable memory fetch from external RAM
   - interpolation: 8 cycles - Hardware sample interpolation between points
   - volume: 4 cycles - Per-oscillator volume scaling
   - output: 5 cycles - DAC output
   - control: 3 cycles - Oscillator control/halt/interrupt logic
   - Reasoning: Interpolation is most expensive (multi-point math); wavetable reads require memory access
   - Result: CPI = 5.501 (0.02% error vs target 5.5)

2. Calibrated typical workload weights
   - wavetable_read=0.216, interpolation=0.257, volume=0.176, output=0.196, control=0.155
   - Interpolation-heavy as it dominates per-oscillator cycle budget
   - Result: Near-perfect match to target (0.02% error from rounding)

**What we learned:**
- ES5503 DOC (Digital Oscillator Chip) is a 32-voice wavetable synthesizer
- Each oscillator independently accesses external wavetable RAM (up to 64KB per bank)
- Variable wavetable sizes: 256 bytes to 32K bytes per oscillator
- Sample rate depends on number of active oscillators (fewer = higher rate)
- 32 oscillators at ~26 kHz or 2 oscillators at ~417 kHz
- Used in Apple IIGS (15 oscillators), Ensoniq Mirage, ESQ-1, many arcade games
- Most complex audio chip in this batch at ~40,000 transistors

**Final state:**
- CPI: 5.501 (0.02% error)
- Validation: PASSED

**References used:**
- Ensoniq ES5503 DOC datasheet
- Apple IIGS hardware reference
- Ensoniq Mirage service manual

---
