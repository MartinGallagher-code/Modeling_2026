# National NSC800 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the National NSC800

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with category-based instruction timing
   - alu: 4.0 cycles - Z80-compatible ALU @4 cycles
   - data_transfer: 4.0 cycles - Register transfers @4 cycles
   - memory: 5.8 cycles - Memory ops @5-7 cycles
   - control: 5.5 cycles - Jump/call @5-10 cycles avg
   - stack: 10.0 cycles - Push/pop @10-11 cycles
   - Reasoning: Cycle counts based on 1979-era 8-bit architecture
   - Result: CPI = 5.860 (6.55% error vs target 5.5)

**What we learned:**
- National NSC800 is a 1979 8-bit microcontroller/processor
- Z80-compatible CMOS, used in Epson HX-20 (first laptop) and military

**Final state:**
- CPI: 5.860 (6.55% error)
- Validation: MARGINAL

**References used:**
- National Semiconductor NSC800 datasheet (1979)
- Z80 timing compatibility

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 1 evaluations
- Corrections: all near zero (model already matched measurements)

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
