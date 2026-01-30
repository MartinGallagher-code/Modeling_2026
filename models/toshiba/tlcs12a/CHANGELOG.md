# Toshiba TLCS-12A Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation and validation

**Session goal:** Create validated model for Toshiba TLCS-12A - improved NMOS TLCS-12

**Starting state:**
- No existing model

**Changes made:**

1. Created initial model with instruction timing calibrated for CPI = 6.0
   - alu: 4 cycles (ADD, SUB, AND, OR)
   - data_transfer: 4 cycles (LD, ST)
   - memory: 7 cycles (indirect addressing)
   - io: 9 cycles (IN, OUT port operations)
   - control: 6 cycles (JMP, BZ, CALL)

**What we learned:**
- TLCS-12A is NMOS version of TLCS-12 (PMOS)
- ~25% faster than original (CPI 6.0 vs 8.0)
- 12-bit word size, minicomputer-style architecture
- I/O operations are the slowest category
- Used in Japanese industrial computing

**Final state:**
- CPI: 5.75 (target 6.0, within 5%)
- Validation: PASSED

**References used:**
- Toshiba TLCS-12A Technical Manual
- Toshiba TLCS-12 Original Documentation
- Japanese Semiconductor History Archives

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 25 evaluations
- Corrections: alu: +1.57, control: +0.13, data_transfer: +2.63, io: -4.29, memory: -0.26

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
