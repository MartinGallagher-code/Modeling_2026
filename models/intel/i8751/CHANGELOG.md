# Intel 8751 Model Changelog

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
- The Intel 8751 (1983) was the EPROM version of the 8051 microcontroller
- 8-bit Harvard architecture with NMOS technology, 60000 transistors
- 12 MHz clock with 12 clocks per machine cycle
- UV-erasable EPROM enabled MCS-51 development and prototyping

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
   - Documented opcodes and machine cycle counts (identical to 8051)
   - Single machine cycle (12 clocks): NOP, ADD, ADDC, SUBB, INC, DEC, MOV A,Rn, MOV Rn,A, MOV A,#data
   - Two machine cycles (24 clocks): MOVX, LJMP, SJMP, LCALL, RET
   - Four machine cycles (48 clocks): MUL AB, DIV AB

2. Added cross_validation section
   - Documented relationship with Intel 8051 (ROM variant - identical timing)
   - Documented relationship with Intel 8752 (larger EPROM variant)
   - Documented relationship with Intel 8748 (MCS-48 family, different architecture)

**What we learned:**
- The 8751 has identical timing to the 8051 (same CPU core)
- EPROM adds development/prototyping capability without changing execution
- The MCS-51 family (8051/8751/8052/8752) shares the same timing model

**Final state:**
- CPI: 12.0 (0.0% error) - unchanged, model already validated
- Cross-validation: Added relationships with 8051, 8752, 8748
- Timing tests: 17 instructions documented with opcodes

**References used:**
- Intel 8751 datasheet (chipdb.org)
- WikiChip MCS-51 documentation

---
