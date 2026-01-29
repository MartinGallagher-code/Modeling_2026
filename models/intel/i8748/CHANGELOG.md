# Intel 8748 Model Changelog

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
- The Intel 8748 (1977) was the EPROM version of the 8048 microcontroller
- 8-bit architecture with NMOS technology, 8000 transistors
- 6 MHz clock with most instructions taking 1-2 cycles
- UV-erasable EPROM allowed for development and prototyping

**Final state:**
- CPI: 1.45 (3.3% error vs expected 1.5)
- Validation: PASSED

---

## 2026-01-28 - Cross-validation with per-instruction timing tests

**Session goal:** Add comprehensive per-instruction timing tests and cross-validation with related processors

**Starting state:**
- CPI: 1.45 (3.3% error vs expected 1.5)
- Model validated but lacked detailed timing tests

**Changes made:**

1. Added 16 per-instruction timing tests to validation JSON
   - Documented opcodes for each instruction (identical to 8048)
   - Single-cycle: NOP, ADD, ADDC, ANL, ORL, XRL, MOV A,Rn, MOV Rn,A, INC A, DEC A
   - Two-cycle: MOV A,#data, MOVX A,@R0, MOVX @R0,A, JMP, CALL, RET

2. Added cross_validation section
   - Documented relationship with Intel 8048 (ROM variant - identical timing)
   - Documented relationship with Intel 8749 (larger EPROM variant)
   - Documented relationship with Intel 8751 (MCS-51 family, different architecture)

**What we learned:**
- The 8748 has identical timing to the 8048 (same CPU core)
- EPROM adds development/prototyping capability without changing execution
- The MCS-48 family (8048/8748/8049/8749) shares the same timing model

**Final state:**
- CPI: 1.45 (3.3% error) - unchanged, model already validated
- Cross-validation: Added relationships with 8048, 8749, 8751
- Timing tests: 16 instructions documented with opcodes

**References used:**
- Intel 8748 datasheet (chipdb.org)
- WikiChip MCS-48 documentation

---
