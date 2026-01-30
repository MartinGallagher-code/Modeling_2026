# AMI S2150 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for AMI S2150

**Changes made:**
1. Created model with same timing as S2000 (CPI=8.0)
2. Added 5 workload profiles and validation tests

**Final state:**
- CPI: 8.0 (0.0% error)
- Validation: PASSED

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 2 evaluations
- Corrections: alu: -1.09, control: +3.58, data_transfer: +2.78, io: -2.87, memory: -2.41

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
