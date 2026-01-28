# Intel 80287 Model Changelog

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
- The Intel 80287 (1983) was the floating-point coprocessor for the 80286
- 80-bit internal precision with NMOS technology, 45000 transistors
- 8 MHz clock, instructions take 50-200 cycles
- Provided hardware floating-point acceleration for scientific computing

**Final state:**
- CPI: 96.9 (3.1% error vs expected 100.0)
- Validation: PASSED

---
