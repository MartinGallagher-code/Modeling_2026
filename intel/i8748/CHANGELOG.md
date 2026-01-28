# Intel 8748 Model Changelog

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
- The Intel 8748 (1977) was the EPROM version of the 8048 microcontroller
- 8-bit architecture with NMOS technology, 8000 transistors
- 6 MHz clock with most instructions taking 1-2 cycles
- UV-erasable EPROM allowed for development and prototyping

**Final state:**
- CPI: 1.45 (3.3% error vs expected 1.5)
- Validation: PASSED

---
