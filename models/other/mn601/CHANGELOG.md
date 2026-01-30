
## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 8 free correction parameters
- Optimizer converged in 22 evaluations
- Corrections: alu_ops: +0.87, io: -1.21, jump: +0.90, memory_read: -0.37, memory_write: -0.88, shift: +0.67, skip: -1.27, stack: -2.52

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
