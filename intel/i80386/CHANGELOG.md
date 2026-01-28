# Intel 80386 Model Changelog

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
- The Intel 80386 (1985) was the first 32-bit x86 processor
- 1.5um CMOS technology with 275000 transistors, 16 MHz clock
- Full 32-bit architecture with virtual memory and paging
- Instructions take 2-40 cycles, enabled running Unix and Windows

**Final state:**
- CPI: 4.335 (3.7% error vs expected 4.5)
- Validation: PASSED

---
