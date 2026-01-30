# AT&T DSP-20 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create initial validated model for AT&T DSP-20 improved Bell Labs DSP

**Starting state:**
- New model, no previous implementation

**Changes made:**

1. Created grey-box queueing model with weighted CPI calculation
   - Implemented instruction categories: mac, alu, data_move, control, io
   - Calibrated for target CPI of 3.0 (improved over DSP-1's 4.0)
   - Created workload profiles for typical, compute, control, io_heavy, mixed

2. Key calibration decisions:
   - MAC: 2 cycles (improved over DSP-1's 3 cycles)
   - ALU: 2 cycles (improved microcode)
   - Data move: 2 cycles (efficient transfers)
   - Control: 4 cycles (improved branching)
   - I/O: 5 cycles (peripheral interface)

**What we learned:**
- DSP-20 improved on DSP-1 with better microcode and doubled clock
- CPI reduced from 4.0 to 3.0 (25% improvement)
- Still primarily Bell Labs internal/captive use
- Bridge between DSP-1 and commercial WE DSP32

**Final state:**
- CPI: 2.95 (1.67% error vs 3.0 expected)
- Validation: PASSED

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 11 evaluations
- Corrections: alu: -5.00, control: +0.80, data_move: +2.53, io: -0.03, mac: +1.53

**Final state:**
- CPI error: 1.44%
- Validation: PASSED

---
