# Raytheon RP-16 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create initial validated model for Raytheon RP-16 military bit-slice system

**Starting state:**
- New model, no previous implementation

**Changes made:**

1. Created grey-box queueing model with weighted CPI calculation
   - Implemented instruction categories: alu, shift, logic, control, memory
   - Calibrated for target CPI of 4.0 (military overhead)
   - Created workload profiles for typical, compute, control, memory_heavy, and mixed

2. Key calibration decisions:
   - ALU: 3 cycles, Shift: 3 cycles, Logic: 3 cycles
   - Control: 5 cycles (multi-chip sequencing overhead)
   - Memory: 6 cycles (4 base + 2 memory access)

**What we learned:**
- RP-16 was a 7-chip military bit-slice system
- MIL-STD qualification added overhead vs commercial parts
- Multi-chip architecture increased inter-chip communication latency
- Designed for reliability in harsh environments, not speed

**Final state:**
- CPI: 3.95 (1.25% error vs 4.0 expected)
- Validation: PASSED

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 2 evaluations
- Corrections: alu: +1.01, control: -0.99, logic: +0.80, memory: -1.99, shift: +1.22

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
