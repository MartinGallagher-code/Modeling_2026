# Intel 8008 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-28 - Initial calibration

**Session goal:** Achieve <5% CPI prediction error

**Starting state:**
- CPI: uncalibrated (high error)
- Key issues: Model used wrong function signature or uncalibrated template

**Changes made:**

1. Rewrote model to use correct analyze() method
   - Replaced simulate() with analyze() returning AnalysisResult
   - Calibrated instruction cycle counts for target CPI
   - Result: Achieved <5% error

**What we learned:**
- The Intel 8008 (1972) was the world's first 8-bit microprocessor
- 10um PMOS technology with 3500 transistors
- 0.5 MHz clock, instructions take 5-11 cycles
- Predecessor to the 8080, ancestor of the x86 family

**Final state:**
- CPI: 11.0 (0.0% error vs expected 11.0)
- Validation: PASSED

---

## 2026-01-28 - Cross-validation with Intel 8080 family

**Session goal:** Cross-validate i8008 against i8080 and i8085 family members

**Starting state:**
- CPI: 11.0 (0.0% error)
- Validation: PASSED

**Changes made:**

1. Added comprehensive timing tests (22 instructions)
   - Data transfer: MOV_r_r, MVI_r (10-16 cycles)
   - Memory: MOV_r_M, MOV_M_r, MVI_M, IN, OUT (12-18 cycles)
   - ALU: ADD_r, ADD_M, ADI, SUB_r, SUB_M, INR_r, DCR_r (10-16 cycles)
   - Control: JMP, CALL, RET, RST, HLT, NOP (8-22 cycles)
   - All timings based on T-states x 2 (cycles per T-state)

2. Added cross_validation section
   - Family comparison with i8080, i8085
   - Instruction timing comparison across all three processors
   - Documented architectural evolution
   - Verified timing consistency across family

**What we learned:**
- i8008 uses T-states (5-11) multiplied by 2 for machine cycles (10-22)
- Significantly slower than 8080/8085 due to PMOS technology
- Different instruction encoding from 8080/8085 (predecessor, not binary compatible)
- JMP/CALL at 22 cycles vs 10/17 cycles on 8080

**Final state:**
- CPI: 11.0 (0.0% error)
- Validation: PASSED
- Cross-validation: Complete

**References used:**
- Intel 8008 datasheet table 2 (instruction timing)
- WikiChip Intel 8008 specifications

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 4 free correction parameters
- Optimizer converged in 1 evaluations
- Corrections: alu: +3.00, control: -7.00, data_transfer: +3.00, memory: -3.00

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
