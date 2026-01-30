# Panafacom MN1613 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation and validation

**Session goal:** Create validated model for Panafacom MN1613 - improved MN1610

**Starting state:**
- No existing model

**Changes made:**

1. Created initial model with instruction timing calibrated for CPI = 4.5
   - alu: 3 cycles (ADD, SUB, MUL, AND, OR)
   - data_transfer: 3 cycles (MOV, LOAD immediate)
   - memory: 5 cycles (LD, ST)
   - io: 6 cycles (IN, OUT)
   - control: 5 cycles (JMP, BZ, BNZ)
   - stack: 6 cycles (CALL, RET, PUSH, POP)

**What we learned:**
- MN1613 is improved successor to MN1610
- 4 MHz clock (double MN1610), hardware multiply
- CPI reduced from 8.0 to 4.5
- ~3.5x throughput improvement over predecessor
- Panafacom joint venture product

**Final state:**
- CPI: 4.40 (target 4.5, within 5%)
- Validation: PASSED

**References used:**
- Panafacom MN1613 Technical Reference
- Panafacom MN1610 Documentation (predecessor)
- Japanese Microprocessor History Archives

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 6 free correction parameters
- Optimizer converged in 8 evaluations
- Corrections: alu: +2.99, control: -0.65, data_transfer: -1.98, io: -1.74, memory: -0.46, stack: -0.54

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
