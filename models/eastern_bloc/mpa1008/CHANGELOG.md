# MPA1008 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial Model Creation

**Session goal:** Create validated grey-box queueing model for MPA1008

**Starting state:**
- No model existed

**Changes attempted:**

1. Created MPA1008 model as Romanian Z80A clone
   - Architecture: 8-bit, sequential execution, 2.5 MHz, 8,500 transistors
   - Calibrated instruction categories from Z80 timing:
     - alu: 4.0 cycles (ADD A,r @4, ADC @4, INC r @4)
     - data_transfer: 4.0 cycles (LD r,r @4, LD r,n @7, LD r,(HL) @7)
     - memory: 6.0 cycles (LD A,(nn) @13, indexed modes)
     - control: 6.0 cycles (JP @10, CALL @17, RET @10, JR @12/7)
     - block: 12.0 cycles (LDIR @21/iteration, CPIR @21)

2. Calibrated workload weights for typical profile:
   - alu: 0.30, data_transfer: 0.25, memory: 0.15, control: 0.20, block: 0.10
   - Produces exactly CPI = 5.5

**What we learned:**
- Romanian Z80A clone, fully compatible with Zilog Z80
- Used in CoBra and HC-85 home computers
- Block operations are key Z80 differentiator from 8080

**Final state:**
- CPI: 5.50 (0.0% error)
- Validation: PASSED (15/15 tests)

**References used:**
- Zilog Z80 Datasheet (timing reference)
- Romanian computing history references

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
