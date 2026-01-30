# Mitsubishi MELPS 4 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for Mitsubishi MELPS 4

**Starting state:**
- No model existed

**Research findings:**
- MELPS 4 (M58840) was Mitsubishi's first 4-bit MCU (1978)
- PMOS technology, 400 kHz clock
- Variable instruction timing: 4-8 cycles
- Used in consumer electronics and appliances

**Changes made:**
1. Created model with variable timing: alu@4, data_transfer@5, memory@7, io@8, control@6
2. Added 5 workload profiles
3. Added validation tests for CPI, weight sums, cycle ranges

**Final state:**
- CPI: 6.0 (target met)
- Validation: PASSED

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 2 evaluations
- Corrections: alu: -0.73, control: +0.94, data_transfer: -0.29, io: +0.09, memory: -0.02

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
