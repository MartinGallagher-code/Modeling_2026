# TI SBP0401 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create initial validated model for TI SBP0401 I2L bit-slice (enhanced control variant)

**Starting state:**
- New model, no previous implementation

**Changes made:**

1. Created grey-box queueing model based on SBP0400 architecture
   - Same instruction categories: alu, shift, logic, control, io
   - Same cycle counts as SBP0400 (target CPI 3.0)
   - Enhanced control description reflecting improved sequencing

2. Key calibration decisions (same as SBP0400):
   - ALU: 2 cycles, Shift: 3 cycles, Logic: 2 cycles
   - Control: 4 cycles, I/O: 5 cycles

**What we learned:**
- SBP0401 is a control-enhanced variant of SBP0400
- Same I2L process and performance envelope
- Enhanced microcode sequencing capability

**Final state:**
- CPI: 3.0 (0.0% error vs 3.0 expected)
- Validation: PASSED

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
