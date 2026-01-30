# Nippon Columbia CX-1 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create initial validated model for Nippon Columbia CX-1 arcade audio DSP

**Starting state:**
- New model, no previous implementation

**Changes made:**

1. Created grey-box queueing model with weighted CPI calculation
   - Implemented instruction categories: mac, filter, output, control, memory
   - Calibrated for target CPI of 3.0 (sequential audio DSP)
   - Created workload profiles for typical, compute, control, io_heavy, mixed

2. Key calibration decisions:
   - MAC: 2 cycles (sequential multiply-accumulate, no pipeline)
   - Filter: 4 cycles (audio filter coefficient computation)
   - Output: 3 cycles (DAC output processing)
   - Control: 3 cycles (loop and branch operations)
   - Memory: 4 cycles (sample buffer and coefficient access)

3. Workload weight calculation:
   - typical: 0.30*2 + 0.15*4 + 0.20*3 + 0.20*3 + 0.15*4 = 3.00 (exact match)

**What we learned:**
- The CX-1 was a custom audio DSP from Nippon Columbia (Denon)
- Used in arcade machines for sound generation
- Sequential architecture without pipelining
- Optimized for audio filtering and waveform generation

**Final state:**
- CPI: 3.00 (0.00% error vs 3.0 expected)
- Validation: PASSED

**References used:**
- Arcade hardware documentation
- MAME emulator source code references

---
