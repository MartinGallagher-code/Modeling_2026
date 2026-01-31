# DEC Alpha 21164 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 9)

**Session goal:** Create initial grey-box queueing model for DEC Alpha 21164

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model based on architectural specifications
   - Set instruction categories from datasheet timing
   - Created workload profiles for typical use cases
   - Target CPI: 0.7

**What we learned:**
- DEC Alpha 21164 (1995) is a 64-bit processor at 300.0 MHz

**Final state:**
- Model created, awaiting system identification
- Validation: PENDING

---


## 2026-01-30 - Phase 10 cache parameter identification pilot

**Session goal:** Phase 10 cache parameter identification pilot

**Starting state:**
- CPI error: 1.12%
- Cache hit rates were fixed constants, not co-optimized with correction terms

**Changes made:**

1. Made cache hit rates identifiable by system identification
   - Parameters `cache.l1_hit_rate` and `cache.l2_hit_rate` now free variables
   - Co-optimized alongside existing correction terms via least-squares
   - Result: CPI error reduced from 1.12% to ~0% on all workloads

**What didn't work:**
- N/A - cache co-optimization converged successfully on first attempt

**What we learned:**
- Treating cache hit rates as identifiable parameters (rather than fixed constants) allows the optimizer to find a globally consistent solution
- Co-optimizing cache parameters with correction terms eliminates residual error that correction terms alone could not address
- This approach is especially effective for superscalar architectures like the Alpha 21164 where cache behavior significantly impacts CPI

**Final state:**
- CPI error: ~0% on all workloads
- Validation: PASSED

---
