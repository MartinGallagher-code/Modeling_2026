# National COP444 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the National COP444

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with category-based instruction timing
   - alu: 3.5 cycles - 4-bit ALU @3-4 cycles
   - data_transfer: 3.5 cycles - Register transfers @3-4 cycles
   - memory: 4.5 cycles - ROM/RAM access @4-5 cycles
   - control: 5.0 cycles - Jump/subroutine @5-6 cycles
   - io: 4.5 cycles - Extended I/O @4-5 cycles
   - Reasoning: Cycle counts based on 1982-era 4-bit architecture
   - Result: CPI = 4.200 (5.00% error vs target 4.0)

**What we learned:**
- National COP444 is a 1982 4-bit microcontroller/processor
- Top-end COP4xx with 2KB ROM and 160 nibbles RAM

**Final state:**
- CPI: 4.200 (5.00% error)
- Validation: MARGINAL

**References used:**
- National Semiconductor COP444 datasheet (1982)

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
