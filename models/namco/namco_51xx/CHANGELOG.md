# Namco 51xx Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial creation

**Session goal:** Create Namco 51xx model for arcade I/O controller chip

**Starting state:**
- New model, no previous version

**Changes made:**

1. Created complete processor model
   - 4-bit custom I/O controller architecture
   - 5 instruction categories: alu, data_transfer, io, control, debounce
   - 4 workload profiles: typical, input_heavy, coin_insert, idle
   - Target CPI: 5.0

2. Created validation JSON with timing data
   - Sources: MAME emulation, community reverse engineering

**Final state:**
- CPI: 5.0 (0% error vs 5.0 expected)
- Validation: PASSED

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 21 evaluations
- Corrections: alu: +0.91, control: -0.24, data_transfer: +2.38, debounce: -2.67, io: -1.14

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
