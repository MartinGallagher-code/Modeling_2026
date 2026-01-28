# Intel 80387 Model Changelog

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
- The Intel 80387 (1987) was the floating-point coprocessor for the 80386
- 80-bit internal precision with CMOS technology, 104000 transistors
- 16 MHz clock, instructions take 20-140 cycles
- Faster than 80287 with improved algorithms

**Final state:**
- CPI: 49.25 (1.5% error vs expected 50.0)
- Validation: PASSED

---
