# Intel 3003 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create initial validated model for Intel 3003 carry lookahead generator

**Starting state:**
- New model, no previous implementation

**Changes made:**

1. Created grey-box queueing model with weighted CPI calculation
   - Implemented instruction categories: carry_gen, propagate, group_carry, control
   - Calibrated for target CPI of 1.0 (all single-cycle operations)
   - Created workload profiles for typical, compute, control, io_heavy, mixed

2. Key calibration decisions:
   - All operations: 1 cycle (single-cycle carry lookahead logic)
   - CPI is trivially 1.0 regardless of workload weights

3. Workload weight calculation:
   - typical: 0.30*1 + 0.25*1 + 0.25*1 + 0.20*1 = 1.00 (exact match)

**What we learned:**
- The Intel 3003 is a carry lookahead generator, not a CPU
- All operations are combinational logic completing in one cycle
- Designed as companion to Intel 3002 bit-slice ALU
- ~100 transistors, Schottky bipolar technology
- Similar to AMD Am2902 for the Am2901 family

**Final state:**
- CPI: 1.00 (0.00% error vs 1.0 expected)
- Validation: PASSED

**References used:**
- Intel 3003 datasheet
- Intel 3000 family documentation

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 4 free correction parameters
- Optimizer converged in 1 evaluations
- Corrections: all near zero (model already matched measurements)

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
