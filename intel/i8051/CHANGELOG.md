# Intel 8051 Model Changelog

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
- The Intel 8051 (1980) is the most successful microcontroller family ever
- 8-bit Harvard architecture with NMOS technology, 60000 transistors
- 12 MHz clock but 12 clocks per machine cycle, so effective CPI is 12+
- MCS-51 architecture still widely used and cloned today

**Final state:**
- CPI: 12.0 (0.0% error vs expected 12.0)
- Validation: PASSED

---
