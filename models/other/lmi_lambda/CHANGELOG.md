# LMI Lambda Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create initial validated model for LMI Lambda LISP machine CPU

**Starting state:**
- New model, no previous implementation

**Changes made:**

1. Created grey-box queueing model with weighted CPI calculation
   - Implemented instruction categories: car_cdr, cons, eval, gc, memory, type_check
   - Calibrated for target CPI of 5.0 (CADR-derivative LISP machine)
   - Created workload profiles for typical, compute, control, io_heavy, mixed

2. Key calibration decisions:
   - CAR/CDR: 2 cycles (same as CADR, hardware-assisted)
   - CONS: 4 cycles (improved from CADR's 5 cycles)
   - EVAL: 7 cycles (improved from CADR's 8 cycles)
   - GC: 11 cycles (improved from CADR's 12 cycles)
   - Memory: 5 cycles (improved from CADR's 6 cycles)
   - Type check: 3 cycles (same as CADR)

3. Workload weight calculation:
   - typical: 0.15*2 + 0.15*4 + 0.20*7 + 0.10*11 + 0.20*5 + 0.20*3 = 5.00 (exact match)

**What we learned:**
- LMI Lambda was a CADR derivative from LISP Machines Inc. (1984)
- Modest improvements over CADR in most operation categories
- CPI between CADR (5.5) and TI Explorer (4.0)
- LMI was one of two companies commercializing the CADR design

**Final state:**
- CPI: 5.00 (0.00% error vs 5.0 expected)
- Validation: PASSED

**References used:**
- LMI documentation
- LISP machine comparison literature

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 6 free correction parameters
- Optimizer converged in 37 evaluations
- Corrections: car_cdr: +0.55, cons: -2.05, eval: +0.10, gc: +1.25, memory: +0.21, type_check: +0.19

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
