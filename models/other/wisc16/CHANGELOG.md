# WISC CPU/16 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial creation

**Session goal:** Create WISC CPU/16 model for 16-bit stack machine

**Starting state:**
- New model, no previous version

**Changes made:**

1. Created complete processor model
   - 16-bit stack machine with writable microcode
   - 5 instruction categories: stack_ops, alu, memory, control, microcode
   - 4 workload profiles: typical, compute, stack_heavy, custom_isa
   - Target CPI: 2.5

**Final state:**
- CPI: 2.40 (4.0% error vs 2.5 expected)
- Validation: PASSED

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 8 evaluations
- Corrections: alu: -0.31, control: +0.53, memory: +0.42, microcode: -0.82, stack_ops: +0.66

**Final state:**
- CPI error: 4.12%
- Validation: PASSED

---
