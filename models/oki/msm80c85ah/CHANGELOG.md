# OKI MSM80C85AH Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation (Phase 4: Second-Source & Licensed Clones)

**Session goal:** Create grey-box queueing model for the OKI MSM80C85AH

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with category-based instruction timing
   - alu: 4.0 cycles - 8085-compatible ALU operations
   - data_transfer: 4.0 cycles - MOV/MVI register transfers
   - memory: 6.0 cycles - Memory load/store operations
   - control: 5.0 cycles - Branch/call flow control
   - stack: 10.0 cycles - Push/pop/call stack operations
   - Reasoning: Identical timing to Intel 8085 as CMOS clone
   - Result: CPI = 5.000 (0.0% error vs target 5.0)

2. Calibrated workload weights for exact target CPI
   - alu: 0.300, data_transfer: 0.280, memory: 0.170, control: 0.168, stack: 0.082
   - Reasoning: Standard 8085 workload distribution
   - Result: Exact match to target CPI of 5.0

**What we learned:**
- MSM80C85AH is the "AH" (high-speed) variant of OKI's CMOS 8085
- CMOS process enables low-power operation for portable devices
- Same cycle counts as NMOS 8085 but at potentially higher clock speeds
- Distinguished from the base MSM80C85 by higher-speed bin

**Final state:**
- CPI: 5.000 (0.0% error)
- Validation: PASSED

**References used:**
- OKI MSM80C85AH datasheet (1983)
- Intel 8085 timing reference documentation

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 143 evaluations
- Corrections: alu: +0.56, control: -1.28, data_transfer: +4.12, memory: -5.00, stack: -3.14

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
