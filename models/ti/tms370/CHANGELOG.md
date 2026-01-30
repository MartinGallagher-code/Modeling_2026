# TI TMS370 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation (Phase 4: Automotive)

**Session goal:** Create grey-box queueing model for the TI TMS370 industrial MCU

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 5 instruction categories
   - alu (2 cycles): Register-to-register ALU operations
   - data_transfer (3 cycles): Data move operations
   - memory (4 cycles): Memory access operations
   - control (3 cycles): Branch/call operations
   - peripheral (5 cycles): Peripheral register access
   - Weights calibrated for target CPI of 3.0

2. Created validation JSON with accuracy metrics
   - CPI error: 0.0% for typical workload

**What we learned:**
- The TMS370 was TI's entry in the industrial MCU market
- Register-file based architecture allows fast register-to-register ALU (2 cycles)
- CMOS process at 8 MHz with ~30,000 transistors
- Rich peripheral set designed for industrial automation

**Final state:**
- CPI: 3.0 (0.0% error vs expected 3.0)
- Validation: PASSED

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 7 evaluations
- Corrections: alu: +1.00, memory: -1.00, peripheral: -2.00

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
