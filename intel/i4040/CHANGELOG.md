# Intel 4040 Model Changelog

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
- The Intel 4040 (1974) was an enhanced version of the 4004 with interrupt support
- 4-bit architecture with 10um PMOS technology, 3000 transistors
- Added halt instruction, interrupt handling, and expanded instruction set
- Same 0.74 MHz clock but more efficient instruction execution

**Final state:**
- CPI: 10.57 (0.7% error vs expected 10.5)
- Validation: PASSED

---
