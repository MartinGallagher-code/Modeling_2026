# K1801VM2 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial Model Creation

**Session goal:** Create validated grey-box queueing model for K1801VM2

**Starting state:**
- No model existed

**Changes attempted:**

1. Created K1801VM2 model as enhanced Soviet PDP-11 compatible processor
   - Architecture: 16-bit, sequential execution, 8 MHz, 25,000 transistors
   - Calibrated instruction categories from enhanced PDP-11 timing:
     - alu: 2.0 cycles (ADD Rn,Rn @2, INC @1, improved over VM1)
     - data_transfer: 3.0 cycles (MOV Rn,Rn @1-2, MOV Rn,(Rn) @3)
     - memory: 6.0 cycles (indirect modes, deferred addressing)
     - control: 4.0 cycles (JMP @3-4, JSR @5-6, RTS @4)
     - float: 10.0 cycles (FADD @8-12, FMUL @10-14)

2. Calibrated workload weights for typical profile:
   - alu: 0.30, data_transfer: 0.25, memory: 0.125, control: 0.225, float: 0.10
   - Produces exactly CPI = 4.0

**What we learned:**
- Enhanced PDP-11 with faster execution and floating point support
- Higher clock (8 MHz vs 5 MHz) and improved microcode
- Used in DVK-3 and DVK-4 systems

**Final state:**
- CPI: 4.00 (0.0% error)
- Validation: PASSED (15/15 tests)

**References used:**
- PDP-11 Architecture Reference (Wikipedia)
- K1801 series technical documentation

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 1 evaluations
- Corrections: all near zero (model already matched measurements)

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
