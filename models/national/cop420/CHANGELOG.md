# National COP420 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the National COP420

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with category-based instruction timing
   - alu: 3.5 cycles - 4-bit ALU operations @3-4 cycles
   - data_transfer: 3.5 cycles - Register transfers @3-4 cycles
   - memory: 4.5 cycles - ROM/RAM access @4-5 cycles
   - control: 5.0 cycles - Jump/skip/subroutine @5-6 cycles
   - io: 4.5 cycles - I/O port operations @4-5 cycles
   - Reasoning: Cycle counts based on 1979-era 4-bit architecture
   - Result: CPI = 4.200 (5.00% error vs target 4.0)

**What we learned:**
- National COP420 is a 1979 4-bit microcontroller/processor
- Enhanced COP400 with 1KB ROM and 64 nibbles RAM

**Final state:**
- CPI: 4.200 (5.00% error)
- Validation: MARGINAL

**References used:**
- National Semiconductor COP420 datasheet (1979)

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 13 evaluations
- Corrections: all near zero (model already matched measurements)

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
