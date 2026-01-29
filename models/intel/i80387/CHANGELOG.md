# Intel 80387 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-28 - Cross-validation and instruction timing tests

**Session goal:** Add per-instruction timing validation and cross-validation with related processors

**Starting state:**
- CPI: 49.25 (1.5% error) - already validated

**Changes made:**

1. Added 12 per-instruction timing tests to validation JSON
   - FLD, FST: 16 cycles (documented: 14-18)
   - FADD, FSUB: 35 cycles (documented: 30-40)
   - FMUL: 65 cycles (documented: 60-70)
   - FDIV: 100 cycles (documented: 95-105)
   - FSQRT: 140 cycles (documented: ~140)
   - FSIN, FCOS, FPTAN: 175 cycles (documented: ~175-180)
   - FLDPI, FXCH: 16 cycles (documented: 12-18)
   - All timings within documented ranges

2. Added cross-validation section
   - Compared with 80287 (predecessor): 80387 is ~2x faster
   - Timing ratios: 0.41x for fp_add, 0.46x for fp_mul, 0.50x for fp_div
   - Consistent with CMOS technology and algorithm improvements
   - 80486 FPU was successor (integrated on-die)

**What we learned:**
- 80387 achieved ~2x speedup over 80287 for arithmetic operations
- Transfer operations (FLD/FST) had smaller speedup (0.80x)
- Transcendental operations (sqrt, trig) had moderate speedup (0.70-0.78x)
- CMOS technology and improved algorithms both contributed

**Final state:**
- CPI: 49.25 (1.5% error vs expected 50.0)
- Validation: PASSED
- Cross-validation: CONSISTENT with 80287

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
- The Intel 80387 (1987) was the floating-point coprocessor for the 80386
- 80-bit internal precision with CMOS technology, 104000 transistors
- 16 MHz clock, instructions take 20-140 cycles
- Faster than 80287 with improved algorithms

**Final state:**
- CPI: 49.25 (1.5% error vs expected 50.0)
- Validation: PASSED

---
