
## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 8 free correction parameters
- Optimizer converged in 14 evaluations
- Corrections: branch: -0.13, call_return: -0.48, immediate: -0.40, io: +0.14, memory_read: -0.08, memory_write: -0.03, register_ops: -0.18, stack: +0.16

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
