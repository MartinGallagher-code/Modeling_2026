# Intel 80186 Model Changelog

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
- The Intel 80186 (1982) integrated 8086 with peripherals on one chip
- 16-bit architecture with NMOS technology, 55000 transistors
- 8 MHz clock with improved instruction timings vs 8086
- Included DMA, timers, and interrupt controller on-chip

**Final state:**
- CPI: 3.85 (3.8% error vs expected 4.0)
- Validation: PASSED

---
