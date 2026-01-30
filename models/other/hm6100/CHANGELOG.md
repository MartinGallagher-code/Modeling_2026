# Harris HM6100 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for Harris HM6100 faster PDP-8

**Starting state:**
- No model existed

**Research findings:**
- Harris HM6100 (1978) was a faster CMOS PDP-8 implementation
- Second-source to Intersil 6100 (IM6100)
- Faster Harris CMOS process technology
- Same 12-bit word size and PDP-8/E instruction set
- State time reduced from 500ns (IM6100) to 400ns
- Full software compatibility with IM6100 and PDP-8/E

**Changes made:**

1. Created model based on Intersil 6100 with ~24% speedup
   - Target CPI: 8.0 states (vs IM6100's 10.5)
   - Faster state time: 400ns vs 500ns
   - Same instruction categories as IM6100

2. Instruction category timing (in states):
   - arithmetic: 8 states (vs 10 on IM6100)
   - logic: 8 states (vs 10 on IM6100)
   - memory: 9 states (vs 12 on IM6100)
   - jump: 9 states (vs 12 on IM6100)
   - io: 9 states (vs 12 on IM6100)
   - operate: 5 states (vs 6 on IM6100)

**What we learned:**
- Harris improved on Intersil's design through better process technology
- Combined CPI improvement and state time reduction = ~65% faster overall
- Full backward compatibility maintained
- Processor family evolution: IM6100 -> HM6100 -> Harris 6120

**Final state:**
- CPI: 8.0 states (0.0% error vs target)
- Validation: PASSED
- At 4 MHz (400ns/state): ~313 KIPS

**References used:**
- Harris HM6100 Datasheet
- Intersil IM6100 Comparison
- CPU-World Harris Semiconductor

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 6 free correction parameters
- Optimizer converged in 33 evaluations
- Corrections: arithmetic: -1.07, io: +3.17, jump: -1.44, logic: -1.23, memory: -0.17, operate: +4.99

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
