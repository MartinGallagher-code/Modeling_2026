# AMI S2000 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for AMI S2000 calculator chip

**Starting state:**
- No model existed

**Research findings:**
- One of the earliest 4-bit calculator chips (1971)
- PMOS technology, 200 kHz clock
- Very slow instruction execution (CPI ~8.0)
- Categories: alu@6, data_transfer@7, memory@9, io@10, control@8

**Changes made:**
1. Created model with variable timing tuned for CPI=8.0
2. Added 5 workload profiles
3. Added validation tests

**Final state:**
- CPI: 8.0 (target met)
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
