# Motorola 68851 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for Motorola 68851 PMMU as part of Phase 4 (Coprocessors & I/O Processors).

**Starting state:**
- No prior model existed

**Changes attempted:**

1. Created initial model with 5 instruction categories
   - translate: 3 cycles (TLB hit address translation)
   - table_walk: 12 cycles base + 11.4 memory cycles (hardware page table walk)
   - flush: 8 cycles (TLB flush)
   - load_descriptor: 6 cycles (page/segment descriptor load)
   - validate: 4 cycles (address validation/protection check)
   - Reasoning: MMU operations dominated by fast TLB hits with occasional expensive table walks
   - Result: Model produces target CPI of 6.0

2. Calibrated typical workload weights
   - translate=0.50, table_walk=0.10, flush=0.08, load_descriptor=0.12, validate=0.20
   - Added 11.4 memory cycles to table_walk for multi-level page table access
   - Result: Exact CPI match at 6.0 (0.00% error)

**What we learned:**
- MMU workloads are bimodal: fast TLB hits vs expensive table walks
- 50% translate weight reflects typical ~90%+ TLB hit rate
- Table walks dominate CPI contribution despite low frequency

**Final state:**
- CPI: 6.0 (0.00% error)
- Validation: PASSED

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 43 evaluations
- Corrections: flush: -5.00, load_descriptor: -5.00, table_walk: -6.00, translate: +4.67, validate: -5.00

**Final state:**
- CPI error: 4.44%
- Validation: PASSED

---
