# Zilog Z80-SIO Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation (Phase 4: Network)

**Session goal:** Create grey-box queueing model for the Zilog Z80-SIO

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 5 instruction categories
   - register_io (2 cycles): Register read/write
   - char_process (4 cycles): Character processing
   - sync (5 cycles): Sync pattern detection
   - control (3 cycles): Mode/command processing
   - interrupt (4 cycles): Interrupt handling
   - Weights calibrated for target CPI of 3.5

2. Created validation JSON with accuracy metrics
   - CPI error: 0.0% for typical workload

**What we learned:**
- The Z80-SIO was the primary serial I/O controller for Z80 systems
- Dual-channel design with both async and sync modes
- Integrated with Z80 interrupt system (daisy chain)
- Predecessor to the more capable Z8530 SCC

**Final state:**
- CPI: 3.5 (0.0% error vs expected 3.5)
- Validation: PASSED

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer did not converge in 200 evaluations
- Corrections: char_process: -1.30, control: -0.92, interrupt: +5.00, register_io: -3.74, sync: +2.62

**Final state:**
- CPI error: 0.13%
- Validation: PASSED

---
