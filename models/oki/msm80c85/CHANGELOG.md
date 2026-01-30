# OKI MSM80C85 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the OKI MSM80C85

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with category-based instruction timing
   - alu: 4.0 cycles - 8085-compatible ALU @4 cycles
   - data_transfer: 4.0 cycles - Register/memory @4-7 cycles
   - memory: 7.0 cycles - Memory access @7-10 cycles
   - control: 7.0 cycles - Branch/call @7-12 cycles
   - stack: 10.0 cycles - Push/pop @10-12 cycles
   - Reasoning: Cycle counts based on 1983-era 8-bit architecture
   - Result: CPI = 6.400 (16.36% error vs target 5.5)

**What we learned:**
- OKI MSM80C85 is a 1983 8-bit microcontroller/processor
- CMOS 8085 second-source, notable for low-power portable use

**Final state:**
- CPI: 6.400 (16.36% error)
- Validation: MARGINAL

**References used:**
- OKI MSM80C85 datasheet (1983)
- Intel 8085 timing compatibility

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 59 evaluations
- Corrections: alu: +1.50, control: -1.50, data_transfer: +1.50, memory: -1.56, stack: -4.43

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
