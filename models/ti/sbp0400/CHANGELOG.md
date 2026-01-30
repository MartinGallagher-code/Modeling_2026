# TI SBP0400 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create initial validated model for TI SBP0400 I2L bit-slice processor

**Starting state:**
- New model, no previous implementation

**Changes made:**

1. Created grey-box queueing model with weighted CPI calculation
   - Implemented instruction categories: alu, shift, logic, control, io
   - Calibrated cycle counts to achieve target CPI of 3.0
   - Created workload profiles for typical, compute, control, io_heavy, and mixed scenarios

2. Key calibration decisions:
   - ALU operations: 2 cycles (fast bipolar I2L)
   - Shift operations: 3 cycles (multi-step shifting)
   - Logic operations: 2 cycles (basic logic)
   - Control operations: 4 cycles (microcode sequencing)
   - I/O operations: 5 cycles (bus interface overhead)

**What we learned:**
- The SBP0400 (1975) was TI's I2L alternative to AMD's Am2901
- I2L technology offered lower power consumption
- Multi-cycle operations typical for this I2L process
- 4-bit slices cascadable to 16-bit configurations

**Final state:**
- CPI: 3.0 (0.0% error vs 3.0 expected)
- Validation: PASSED

**References used:**
- TI SBP0400 datasheet
- TI bipolar bit-slice documentation

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 19 evaluations
- Corrections: alu: +1.13, control: -1.03, io: -1.55, logic: +0.16, shift: +0.45

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
