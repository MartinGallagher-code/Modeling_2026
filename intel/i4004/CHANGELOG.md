# Intel 4004 Model Changelog

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
- The Intel 4004 (1971) was the world's first commercial microprocessor
- 4-bit architecture with 10um PMOS technology, only 2300 transistors
- Clock speed of 0.74 MHz, instructions take 8-16 cycles (1-2 machine cycles)
- Each machine cycle is 8 clock cycles, so effective CPI is very high

**Final state:**
- CPI: 10.6 (1.9% error vs expected 10.8)
- Validation: PASSED

---
