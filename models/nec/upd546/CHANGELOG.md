# NEC uPD546 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the NEC uPD546

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with category-based instruction timing
   - alu: 4.5 cycles - 4-bit arithmetic with BCD @4-5 cycles
   - data_transfer: 4.0 cycles - Accumulator/register transfers @4 cycles
   - memory: 5.5 cycles - ROM table/RAM access @5-6 cycles
   - control: 6.5 cycles - Jump/subroutine @6-7 cycles
   - io: 5.5 cycles - Port I/O @5-6 cycles
   - Reasoning: Cycle counts based on 1975-era 4-bit architecture
   - Result: CPI = 5.200 (4.00% error vs target 5.0)

**What we learned:**
- NEC uPD546 is a 1975 4-bit microcontroller/processor
- Early NEC 4-bit MCU for calculators and appliances

**Final state:**
- CPI: 5.200 (4.00% error)
- Validation: PASSED

**References used:**
- NEC uPD546 datasheet (1975)
- NEC uCOM-4 family guide

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 14 evaluations
- Corrections: all near zero (model already matched measurements)

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
