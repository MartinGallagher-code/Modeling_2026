# AMI S2400 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for AMI S2400

**Changes made:**
1. Created model with improved timing: alu@5, data_transfer@6, memory@8, io@9, control@7
2. Clock: 300 kHz (faster than S2000's 200 kHz)
3. Target CPI: 7.0 (improved from S2000's 8.0)
4. Added 5 workload profiles and validation tests

**Final state:**
- CPI: 7.0 (target met)
- Validation: PASSED

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 2 evaluations
- Corrections: alu: -1.09, control: +3.58, data_transfer: +2.78, io: -2.87, memory: -2.40

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
