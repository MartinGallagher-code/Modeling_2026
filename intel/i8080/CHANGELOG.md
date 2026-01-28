# Intel 8080 Model Changelog

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
- The Intel 8080 (1974) was the industry standard 8-bit CPU
- 6um NMOS technology with 4500 transistors, 2 MHz clock
- Instructions take 4-18 cycles depending on type
- Direct ancestor of the x86 architecture, powered the Altair 8800

**Final state:**
- CPI: 9.075 (1.4% error vs expected 9.2)
- Validation: PASSED

---
