# Intel 8751 Model Changelog

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
- The Intel 8751 (1983) was the EPROM version of the 8051 microcontroller
- 8-bit Harvard architecture with NMOS technology, 60000 transistors
- 12 MHz clock with 12 clocks per machine cycle
- UV-erasable EPROM enabled MCS-51 development and prototyping

**Final state:**
- CPI: 12.0 (0.0% error vs expected 12.0)
- Validation: PASSED

---
