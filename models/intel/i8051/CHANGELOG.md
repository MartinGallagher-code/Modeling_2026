# Intel 8051 Model Changelog

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
- The Intel 8051 (1980) is the most successful microcontroller family ever
- 8-bit Harvard architecture with NMOS technology, 60000 transistors
- 12 MHz clock but 12 clocks per machine cycle, so effective CPI is 12+
- MCS-51 architecture still widely used and cloned today

**Final state:**
- CPI: 12.0 (0.0% error vs expected 12.0)
- Validation: PASSED

---

## 2026-01-28 - Cross-validation with per-instruction timing tests

**Session goal:** Add comprehensive per-instruction timing tests and cross-validation with related processors

**Starting state:**
- CPI: 12.0 (0.0% error vs expected 12.0)
- Model validated but lacked detailed timing tests

**Changes made:**

1. Added 17 per-instruction timing tests to validation JSON
   - Documented opcodes and machine cycle counts for each instruction
   - Single machine cycle (12 clocks): NOP, ADD, ADDC, SUBB, INC, DEC, MOV A,Rn, MOV Rn,A, MOV A,#data
   - Two machine cycles (24 clocks): MOVX, LJMP, SJMP, LCALL, RET
   - Four machine cycles (48 clocks): MUL AB, DIV AB

2. Added cross_validation section
   - Documented relationship with Intel 8751 (EPROM variant - identical timing)
   - Documented relationship with Intel 8052 (larger memory variant)
   - Documented relationship with Intel 8048 (predecessor, different architecture)

**What we learned:**
- The 8051 has 12 clock cycles per machine cycle (1 us at 12 MHz)
- All instruction timing is in multiples of 12 clocks
- MUL and DIV are the slowest instructions at 4 machine cycles

**Final state:**
- CPI: 12.0 (0.0% error) - unchanged, model already validated
- Cross-validation: Added relationships with 8751, 8052, 8048
- Timing tests: 17 instructions documented with opcodes

**References used:**
- Intel 8051 datasheet (chipdb.org)
- WikiChip MCS-51 documentation

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 4 free correction parameters
- Optimizer converged in 1 evaluations
- Corrections: all near zero (model already matched measurements)

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
