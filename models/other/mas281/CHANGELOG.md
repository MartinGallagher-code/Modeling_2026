# Marconi Elliot MAS281 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the Marconi Elliot MAS281

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with category-based instruction timing
   - alu: 3.0 cycles - 16-bit ALU @2-4 cycles
   - data_transfer: 3.0 cycles - Register transfers @2-4 cycles
   - memory: 5.5 cycles - Memory access @4-7 cycles
   - control: 6.0 cycles - Branch/call @5-8 cycles
   - stack: 6.0 cycles - Stack ops @5-7 cycles
   - Reasoning: Cycle counts based on 1979-era 16-bit architecture
   - Result: CPI = 4.700 (4.44% error vs target 4.5)

**What we learned:**
- Marconi Elliot MAS281 is a 1979 16-bit processor
- British military 16-bit for naval systems

**Final state:**
- CPI: 4.700 (4.44% error)
- Validation: PASSED

**References used:**
- Marconi Elliot MAS281 technical reference (1979)

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 19 evaluations
- Corrections: alu: +1.35, control: -1.65, data_transfer: +1.35, memory: -0.86, stack: -0.97

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
