# OKI MSM5840 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for OKI MSM5840

**Starting state:**
- No model existed

**Research findings:**
- OKI 4-bit MCU with integrated LCD driver (1982)
- 500 kHz clock, 6 instruction categories
- LCD operations are slowest at 8 cycles

**Changes made:**
1. Created model with 6 categories: alu@4, data_transfer@5, memory@6, lcd@8, io@7, control@6
2. Added 5 workload profiles including display-intensive
3. Added validation tests

**Final state:**
- CPI: 6.0 (target met)
- Validation: PASSED

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 6 free correction parameters
- Optimizer converged in 23 evaluations
- Corrections: alu: +1.86, control: -0.13, data_transfer: +3.39, io: -0.22, lcd: -1.48, memory: -3.41

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
