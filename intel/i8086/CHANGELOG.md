# Intel 8086 Model Changelog

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
- The Intel 8086 (1978) was the first x86 processor, foundation of the x86 architecture
- 3um NMOS technology with 29000 transistors, 5 MHz clock
- 16-bit architecture with segment registers for 20-bit addressing (1MB)
- Instructions take 2-200+ cycles, with MUL/DIV being very expensive

**Final state:**
- CPI: 4.525 (0.6% error vs expected 4.5)
- Validation: PASSED

---
