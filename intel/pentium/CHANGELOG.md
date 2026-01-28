# Intel Pentium Model Changelog

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
- The Intel Pentium (1993) was the first superscalar x86 processor
- 0.8um CMOS technology with 3.1 million transistors, 60 MHz base clock
- Dual pipelines (U and V) can issue 2 instructions per cycle
- Separate I/D caches (8KB each) and dynamic branch prediction

**Final state:**
- CPI: 0.985 (1.5% error vs expected 1.0)
- Validation: PASSED

---
