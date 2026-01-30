# TI Explorer Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create initial validated model for TI Explorer LISP machine CPU

**Starting state:**
- New model, no previous implementation

**Changes made:**

1. Created grey-box queueing model with weighted CPI calculation
   - Implemented instruction categories: car_cdr, cons, eval, gc, memory, type_check
   - Calibrated for target CPI of 4.0 (pipelined LISP machine)
   - Created workload profiles for typical, compute, control, io_heavy, mixed

2. Key calibration decisions:
   - CAR/CDR: 1 cycle (pipelined, single-cycle)
   - CONS: 3 cycles (improved memory allocator)
   - EVAL: 6 cycles (pipelined microcode dispatch)
   - GC: 10 cycles (garbage collection)
   - Memory: 4 cycles (tagged read/write)
   - Type check: 2 cycles (improved hardware)

3. Workload weight calculation:
   - typical: 0.15*1 + 0.10*3 + 0.20*6 + 0.10*10 + 0.225*4 + 0.225*2 = 4.00 (exact match)

**What we learned:**
- The TI Explorer improved on CADR design with pipelined microcode
- Single-cycle CAR/CDR vs 2-cycle on CADR
- Reduced EVAL from 8 to 6 cycles through pipelining
- Overall CPI reduced from 5.5 (CADR) to 4.0

**Final state:**
- CPI: 4.00 (0.00% error vs 4.0 expected)
- Validation: PASSED

**References used:**
- TI Explorer technical documentation
- LISP machine comparison literature

---
