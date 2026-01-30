
## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 8 free correction parameters
- Optimizer converged in 20 evaluations
- Corrections: branch: +0.12, byte: -1.45, immediate: +0.53, jsr: +1.09, memory_read: -0.24, memory_write: +0.24, register_ops: +0.55, trap: -4.52

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
