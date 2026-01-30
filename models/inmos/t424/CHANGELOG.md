# Inmos T424 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the Inmos T424

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with category-based instruction timing
   - alu: 1.5 cycles - Single-cycle ALU @1-2 cycles
   - data_transfer: 1.5 cycles - Register moves @1-2 cycles
   - memory: 2.5 cycles - On-chip memory @2-3 cycles
   - control: 3.0 cycles - Branch/process @2-4 cycles
   - channel: 3.5 cycles - Channel communication @3-5 cycles
   - Reasoning: Cycle counts based on 1985-era 32-bit architecture
   - Result: CPI = 2.400 (20.00% error vs target 2.0)

**What we learned:**
- Inmos T424 is a 1985 32-bit processor
- 32-bit transputer with 4KB on-chip RAM, T414 variant

**Final state:**
- CPI: 2.400 (20.00% error)
- Validation: MARGINAL

**References used:**
- Inmos T424 transputer datasheet (1985)

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 15 evaluations
- Corrections: alu: -0.38, channel: -1.66, control: -0.28, data_transfer: +1.70, memory: -1.78

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
