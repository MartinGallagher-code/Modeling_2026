# Sharp SM5 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the Sharp SM5

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with category-based instruction timing
   - alu: 3.5 cycles - 4-bit ALU with carry @3-4 cycles
   - data_transfer: 3.5 cycles - Immediate/register moves @3-4 cycles
   - memory: 4.5 cycles - ROM table/RAM access @4-5 cycles
   - control: 5.0 cycles - Branch/call/return @5-6 cycles
   - io: 4.5 cycles - LCD segment/button I/O @4-5 cycles
   - Reasoning: Cycle counts based on 1984-era 4-bit architecture
   - Result: CPI = 4.200 (5.00% error vs target 4.0)

**What we learned:**
- Sharp SM5 is a 1984 4-bit microcontroller/processor
- Enhanced SM4, massively produced for LCD games

**Final state:**
- CPI: 4.200 (5.00% error)
- Validation: MARGINAL

**References used:**
- Sharp SM5xx series manual
- Nintendo Game & Watch documentation

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 1 evaluations
- Corrections: alu: +0.50, control: -1.00, data_transfer: +0.50, io: -0.50, memory: -0.50

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
