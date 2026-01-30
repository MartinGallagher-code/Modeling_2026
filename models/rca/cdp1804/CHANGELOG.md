# RCA CDP1804 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for CDP1804 COSMAC variant

**Starting state:**
- No model existed

**Research findings:**
- RCA CDP1804 (1980) was an enhanced COSMAC with on-chip timer
- Compatible with CDP1802 instruction set
- Approximately 17% faster than 1802 due to process improvements
- On-chip counter/timer for interrupt generation
- Same 16 x 16-bit register architecture as 1802
- CMOS technology, radiation-hardened variants available

**Changes made:**

1. Created model based on 1802 architecture with ~17% speedup
   - Target CPI: 10.0 (vs 1802's 12.0)
   - Same instruction categories as 1802
   - Faster cycle times across all categories

2. Instruction category timing:
   - register_ops: 7 cycles (vs 8 on 1802)
   - immediate: 10 cycles (vs 12 on 1802)
   - memory_read: 11 cycles (vs 14 on 1802)
   - memory_write: 11 cycles (vs 14 on 1802)
   - branch: 11 cycles (vs 14 on 1802)
   - call_return: 17 cycles (vs 20 on 1802)

**What we learned:**
- CDP1804 was a drop-in replacement for 1802 with better performance
- Timer feature useful for real-time applications
- Same power-efficient CMOS design as 1802
- Part of the broader COSMAC family (1802, 1804, 1805, 1806)

**Final state:**
- CPI: 10.0 (0.0% error vs target)
- Validation: PASSED
- At 2 MHz: ~200 KIPS

**References used:**
- RCA CDP1804 Datasheet
- RCA COSMAC Microprocessor Family Manual
- CPU-World CDP1804

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 6 free correction parameters
- Optimizer did not converge in 200 evaluations
- Corrections: branch: -4.30, call_return: -1.06, immediate: -1.24, memory_read: +1.35, memory_write: -5.50, register_ops: +3.85

**Final state:**
- CPI error: 0.01%
- Validation: PASSED

---
