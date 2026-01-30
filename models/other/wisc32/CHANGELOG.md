# WISC CPU/32 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial creation

**Session goal:** Create WISC CPU/32 model for 32-bit stack machine

**Starting state:**
- New model, no previous version

**Changes made:**

1. Created complete processor model
   - 32-bit stack machine with writable microcode (evolution of CPU/16)
   - 5 instruction categories: stack_ops, alu, memory, control, microcode
   - 4 workload profiles: typical, compute, stack_heavy, custom_isa
   - Target CPI: 2.0 (improved from CPU/16's 2.5)

**Final state:**
- CPI: 1.93 (3.75% error vs 2.0 expected)
- Validation: PASSED

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 19 evaluations
- Corrections: alu: -0.19, control: +0.45, memory: +0.24, microcode: -0.04, stack_ops: +0.39

**Final state:**
- CPI error: 4.12%
- Validation: PASSED

---
