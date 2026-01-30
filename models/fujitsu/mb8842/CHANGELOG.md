# Fujitsu MB8842 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for Fujitsu MB8842 arcade MCU

**Starting state:**
- No model existed

**Research findings:**
- MB8842 is an MB8841 variant for arcade applications
- Same instruction set and timing as MB8841
- Used in Namco arcade hardware
- Fixed 4-cycle instruction timing
- 1 MHz clock, 4-bit data path

**Changes made:**

1. Created model with fixed 4-cycle instruction timing (same as MB8841)
   - Target CPI: 4.0
   - All instruction categories set to 4 cycles
   - Clock: 1 MHz

2. Added 5 instruction categories (alu, data_transfer, memory, control, io)
3. Added 5 workload profiles (typical, compute, memory, control, mixed)
4. Added validation tests for CPI accuracy, weight sums, cycle ranges, all workloads

**Final state:**
- CPI: 4.0 (0.0% error)
- Validation: PASSED

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 1 evaluations
- Corrections: all near zero (model already matched measurements)

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
