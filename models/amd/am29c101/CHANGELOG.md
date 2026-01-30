# AMD Am29C101 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create initial validated model for AMD Am29C101 CMOS bit-slice

**Starting state:**
- New model, no previous implementation

**Changes made:**

1. Created grey-box queueing model with weighted CPI calculation
   - Implemented instruction categories: alu, shift, logic, control, cascade
   - Calibrated for target CPI of 2.5
   - Created workload profiles for typical, compute, control, cascaded, and mixed

2. Key calibration decisions:
   - ALU: 2 cycles, Shift: 2.5 cycles, Logic: 2 cycles
   - Control: 3 cycles, Cascade: 3 cycles
   - Slightly higher CPI than discrete Am2901 due to CMOS speed

**What we learned:**
- Am29C101 integrated four Am2901s into single CMOS chip
- CMOS trades some speed for dramatically lower power
- 20000 transistors (significant integration for 1982)

**Final state:**
- CPI: 2.5 (0.0% error vs 2.5 expected)
- Validation: PASSED

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 1 evaluations
- Corrections: alu: +0.50, cascade: -0.50, control: -0.50, logic: +0.50

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
