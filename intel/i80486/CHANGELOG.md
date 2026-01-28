# Intel 80486 Model Changelog

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
- The Intel 80486 (1989) was the first pipelined x86 with on-chip cache and FPU
- 1um CMOS technology with 1.2 million transistors, 25 MHz base clock
- 5-stage pipeline enabled many instructions to complete in 1 cycle
- First x86 to break 1 MIPS/MHz barrier

**Final state:**
- CPI: 2.05 (2.5% error vs expected 2.0)
- Validation: PASSED

---
