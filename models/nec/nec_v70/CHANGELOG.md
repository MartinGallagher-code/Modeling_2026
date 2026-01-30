# NEC V70 Model Changelog

**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create and validate NEC V70 model

**Starting state:** No model existed

**Changes:**
1. Created model based on V60 architecture with slightly improved CPI (2.8 vs 3.0)
2. 6 instruction categories: ALU, data transfer, memory, control, float, string
3. 4 workload profiles: typical, compute, memory, control

**Final state:**
- CPI: 2.825 (0.89% error)
- Validation: PASSED (9/9 tests)

**References used:**
- NEC V60/V70 User Manual

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 6 free correction parameters
- Optimizer converged in 11 evaluations
- Corrections: alu: -0.04, control: -0.08, data_transfer: -0.05, float: -0.09, memory: -0.02, string: -0.09

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
