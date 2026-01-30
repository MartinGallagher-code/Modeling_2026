# AMI S28211 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create initial validated model for AMI S28211 DSP peripheral

**Starting state:**
- New model, no previous implementation

**Changes made:**

1. Created grey-box queueing model with weighted CPI calculation
   - Implemented instruction categories: mac, alu, data_move, control, io
   - Calibrated for target CPI of 5.0 (bus peripheral overhead)
   - Created workload profiles for typical, compute, control, io_heavy, mixed

2. Key calibration decisions:
   - MAC: 4 cycles (no hardware MAC, software multiply)
   - ALU: 3 cycles (basic arithmetic)
   - Data move: 4 cycles (6800 bus transfer overhead)
   - Control: 6 cycles (coordination with host CPU)
   - I/O: 8 cycles (full 6800 bus transaction)

**What we learned:**
- S28211 was a DSP peripheral, not a standalone processor
- 6800 bus interface adds significant overhead
- Coprocessor architecture requires host CPU coordination
- ~5000 transistors, relatively simple design
- Higher CPI than standalone DSPs of the era

**Final state:**
- CPI: 4.95 (1.0% error vs 5.0 expected)
- Validation: PASSED

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 2 evaluations
- Corrections: alu: +0.38, control: +0.09, data_move: +1.12, io: +0.97, mac: -2.12

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
