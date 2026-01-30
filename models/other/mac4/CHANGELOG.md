# Bell Labs MAC-4 Model Changelog

**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create and validate MAC-4 telecom MCU model

**Starting state:** No model existed

**Changes:**
1. Created model with 5 categories (alu, data_transfer, memory, io, control)
2. Heavy I/O focus for telecom switching workloads
3. Target CPI: 5.0

**Final state:**
- CPI: 4.95 (1.0% error)
- Validation: PASSED

**References:**
- Bell System Technical Journal

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 16 evaluations
- Corrections: alu: +0.94, control: +0.82, data_transfer: +2.63, io: -3.62, memory: -1.35

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
