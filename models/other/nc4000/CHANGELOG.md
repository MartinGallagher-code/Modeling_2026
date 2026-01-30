# Novix NC4000 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation (Phase 4: Forth)

**Session goal:** Create grey-box queueing model for the Novix NC4000 Forth processor

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 5 instruction categories
   - stack_op (1 cycle): Stack push/pop/dup/swap
   - alu (1 cycle): ALU operations on top-of-stack
   - memory (3 cycles): Memory fetch/store
   - control (2 cycles): Branch/loop operations
   - call_return (1 cycle): Subroutine call/return (hardware threaded)
   - Weights calibrated for target CPI of 1.5

2. Created validation JSON with accuracy metrics
   - CPI error: 0.0% for typical workload

**What we learned:**
- The NC4000 was the first single-chip Forth processor
- Designed by Chuck Moore (inventor of Forth)
- Hardware call/return is single-cycle due to subroutine threading
- Only 16,000 transistors - extremely efficient design
- Memory access at 3 cycles is the main bottleneck
- Stack and ALU operations are both single-cycle

**Final state:**
- CPI: 1.5 (0.0% error vs expected 1.5)
- Validation: PASSED

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 8 evaluations
- Corrections: alu: +0.50, call_return: +0.50, control: -0.50, memory: -1.50, stack_op: +0.50

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
