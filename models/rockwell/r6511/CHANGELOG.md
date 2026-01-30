# Rockwell R6511 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create initial R6511 model based on 6502 timing

**Starting state:**
- No model existed

**Changes made:**

1. Created R6511 model based on MOS 6502 timing
   - The R6511 is a 6502-based microcontroller with integrated peripherals
   - Same instruction set and timing as MOS 6502
   - Calibrated for CPI = 3.0

2. Created validation JSON with timing tests
   - Same instruction timing as 6502
   - 2-7 cycles per instruction

3. Created documentation files

**What we learned:**
- The Rockwell R6511 (1980) is a 6502-variant microcontroller
- 8-bit architecture with integrated RAM, ROM, I/O, and timer
- Fully 6502-compatible instruction set and timing
- Used in embedded control applications

**Final state:**
- CPI: 3.0 (target)
- Validation: PASSED

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 18 evaluations
- Corrections: alu: +0.65, control: +0.77, data_transfer: +0.10, memory: -0.85, stack: -1.42

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
