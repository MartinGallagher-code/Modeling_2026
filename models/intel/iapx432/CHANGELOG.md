# Intel iAPX 432 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-28 - Cross-validation and instruction timing tests

**Session goal:** Add per-instruction timing validation and cross-validation with related processors

**Starting state:**
- CPI: 48.25 (3.5% error) - already validated

**Changes made:**

1. Added 12 per-instruction timing tests to validation JSON
   - ADD/SUBTRACT_INTEGER: 25 cycles (documented: 20-30) - includes capability check
   - MOVE_DATA, COPY_OBJECT: 35 cycles (documented: 30-45)
   - LOAD/STORE with capability: 60 cycles (documented: 50-75)
   - BRANCH, CALL_PROCEDURE: 50 cycles (documented: 40-80)
   - CREATE/DELETE_OBJECT: 120 cycles (documented: 80-400+)
   - SEND_MESSAGE (Ada tasking): 120 cycles (documented: 100-200)
   - CHECK_RIGHTS: 25 cycles (documented: 15-35)
   - All timings within documented ranges

2. Added cross-validation section
   - Compared with Intel 8086: iAPX 432 is 5-10x slower
   - Timing ratios: ALU 8.3x, data 8.75x, memory 6.0x, branch 3.1x
   - Consistent with known commercial failure
   - 68000 and 80286 won the market due to simplicity

**What we learned:**
- Every iAPX 432 operation includes capability checking overhead
- Object creation/deletion was extremely expensive (hardware GC support)
- The architecture was designed for Ada, which added further overhead
- Intel's decision to abandon capability-based approach was correct
- High CPI (~50) accurately reflects the architectural complexity

**Final state:**
- CPI: 48.25 (3.5% error vs expected 50.0)
- Validation: PASSED
- Cross-validation: CONSISTENT with 8086 (5-10x slower as documented)

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
- The Intel iAPX 432 (1981) was Intel's failed capability-based architecture
- 32-bit object-oriented architecture with NMOS technology, 250000 transistors
- 8 MHz clock but extremely high CPI due to capability checking
- Instructions take 6-400+ cycles, making it 5-10x slower than 8086

**Final state:**
- CPI: 48.25 (3.5% error vs expected 50.0)
- Validation: PASSED

---
