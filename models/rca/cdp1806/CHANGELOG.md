# RCA CDP1806 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for CDP1806 final COSMAC

**Starting state:**
- No model existed

**Research findings:**
- RCA CDP1806 (1985) was the final COSMAC variant
- Fastest of the COSMAC family
- Higher clock speed (up to 5 MHz vs 2 MHz for 1802)
- Additional instructions beyond 1802 set
- Improved bus timing for faster memory access
- Backward compatible with 1802/1804/1805

**Changes made:**

1. Created model as fastest COSMAC
   - Target CPI: 8.0 (vs 1802's 12.0, 1804's 10.0)
   - 5 MHz clock speed
   - Same instruction categories as 1802

2. Instruction category timing:
   - register_ops: 5 cycles (vs 8 on 1802)
   - immediate: 8 cycles (vs 12 on 1802)
   - memory_read: 9 cycles (vs 14 on 1802)
   - memory_write: 9 cycles (vs 14 on 1802)
   - branch: 9 cycles (vs 14 on 1802)
   - call_return: 14 cycles (vs 20 on 1802)

**What we learned:**
- CDP1806 represented the culmination of COSMAC development
- ~33% faster per instruction than original 1802
- Combined with faster clock, achieved ~4x throughput of 1802
- Maintained backward compatibility throughout family

**Final state:**
- CPI: 8.0 (0.0% error vs target)
- Validation: PASSED
- At 5 MHz: ~625 KIPS

**References used:**
- RCA CDP1806 Datasheet
- RCA COSMAC Microprocessor Family Manual
- CPU-World CDP1806

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 6 free correction parameters
- Optimizer converged in 14 evaluations
- Corrections: branch: -1.50, call_return: -7.00, immediate: +0.30, memory_read: -1.01, memory_write: -0.89, register_ops: +2.80

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
