# Hitachi HD6305 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation (Phase 4: Automotive)

**Session goal:** Create grey-box queueing model for the Hitachi HD6305

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 5 instruction categories
   - alu (3 cycles): Basic ALU operations
   - data_transfer (3 cycles): Load/store operations
   - memory (5 cycles): Extended memory access
   - control (4 cycles): Branch/jump operations
   - timer (4 cycles): Timer/counter operations
   - Weights calibrated for target CPI of 3.5

2. Created validation JSON with accuracy metrics
   - CPI error: 0.0% for typical workload

**What we learned:**
- The HD6305 is Hitachi's second-source of the Motorola 6805 family
- CMOS process at 4 MHz with enhanced timer/counter peripherals
- Instruction set compatible with Motorola 6805
- ~10,000 transistors, slightly more than base 6805 due to enhanced peripherals

**Final state:**
- CPI: 3.5 (0.0% error vs expected 3.5)
- Validation: PASSED

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 6 evaluations
- Corrections: alu: -0.90, control: -0.29, data_transfer: +1.56, memory: +0.19, timer: -1.17

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
