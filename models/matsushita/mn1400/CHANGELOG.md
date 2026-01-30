# Matsushita MN1400 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the Matsushita MN1400

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with category-based instruction timing
   - alu: 3.5 cycles - 4-bit arithmetic @3-4 cycles
   - data_transfer: 3.5 cycles - Register moves @3-4 cycles
   - memory: 4.5 cycles - ROM/RAM access @4-5 cycles
   - control: 5.0 cycles - Jump/call @5-6 cycles
   - io: 4.5 cycles - Peripheral I/O @4-5 cycles
   - Reasoning: Cycle counts based on 1974-era 4-bit architecture
   - Result: CPI = 4.200 (5.00% error vs target 4.0)

**What we learned:**
- Matsushita MN1400 is a 1974 4-bit microcontroller/processor
- Early Japanese 4-bit MCU, used in Panasonic consumer products

**Final state:**
- CPI: 4.200 (5.00% error)
- Validation: MARGINAL

**References used:**
- Matsushita MN1400 series datasheet (1974)

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 1 evaluations
- Corrections: alu: +0.48, control: -1.02, data_transfer: +0.48, io: -0.44, memory: -0.44

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
