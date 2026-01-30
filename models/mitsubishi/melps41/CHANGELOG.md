# Mitsubishi MELPS 41 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for Mitsubishi MELPS 41

**Starting state:**
- No model existed

**Research findings:**
- Enhanced MELPS 4 with NMOS technology (1980)
- 500 kHz clock, improved timing
- CPI ~5.5 (better than MELPS 4's 6.0)

**Changes made:**
1. Created model with variable timing: alu@4, data_transfer@5, memory@6, io@7, control@5.5
2. Added 5 workload profiles
3. Added validation tests

**Final state:**
- CPI: 5.5 (target met)
- Validation: PASSED

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 2 evaluations
- Corrections: alu: -1.15, control: +2.02, data_transfer: +1.23, io: -1.02, memory: -1.07

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
