# Intel 80286 Model Changelog

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
- The Intel 80286 (1982) introduced protected mode to x86
- 1.5um CMOS technology with 134000 transistors, 8 MHz clock
- 16-bit architecture with 24-bit addressing (16MB)
- Instructions take 2-25 cycles, faster than 8086 for most operations

**Final state:**
- CPI: 4.0 (0.0% error vs expected 4.0)
- Validation: PASSED

---
