# Intel iAPX 432 Model Changelog

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
- The Intel iAPX 432 (1981) was Intel's failed capability-based architecture
- 32-bit object-oriented architecture with NMOS technology, 250000 transistors
- 8 MHz clock but extremely high CPI due to capability checking
- Instructions take 6-400+ cycles, making it 5-10x slower than 8086

**Final state:**
- CPI: 48.25 (3.5% error vs expected 50.0)
- Validation: PASSED

---
