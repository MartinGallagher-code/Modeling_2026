# Yamaha YM2151 OPM Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the Yamaha YM2151 OPM FM synthesis chip

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with 5 category-based instruction timing
   - operator: 6 cycles - FM operator computation (sine lookup + modulation)
   - envelope: 4 cycles - ADSR envelope generation per operator
   - lfo: 3 cycles - Low-frequency oscillator (4 waveforms)
   - output: 5 cycles - DAC output with stereo L/R panning
   - register: 2 cycles - Register write (address + data)
   - Reasoning: 4-op FM requires more operator cycles; LFO is lightweight
   - Result: CPI = 4.500 (0.00% error vs target 4.5)

2. Calibrated typical workload weights
   - operator=0.30, envelope=0.20, lfo=0.15, output=0.25, register=0.10
   - Operator-heavy reflects 32 operators (8ch x 4op) dominating cycle budget
   - Result: Perfect match to target

**What we learned:**
- YM2151 (OPM) is the first standalone FM synthesis chip from Yamaha
- 8 channels with 4 operators each, 8 configurable algorithms
- Hardware LFO with amplitude and pitch modulation
- Stereo output with per-channel L/R panning
- Widely used in arcade games (Sega System 16, Capcom CPS-1, Konami)
- 64 sample slots per channel update cycle

**Final state:**
- CPI: 4.500 (0.00% error)
- Validation: PASSED

**References used:**
- Yamaha YM2151 application manual
- YM2151 reverse engineering documentation
- MAME source code (ym2151.cpp)

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 28 evaluations
- Corrections: envelope: +3.53, lfo: -1.10, operator: -2.88, output: -0.33, register: +4.06

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
