# AMD Am386 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for AMD Am386

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: alu (2.0 cyc), data_transfer (2.0 cyc), memory (4.0 cyc), control (8.0 cyc), multiply (12.0 cyc), divide (38.0 cyc)
   - Architecture: AMD's 386 clone, 40 MHz (faster than Intel's 33 MHz)
   - Target CPI: 4.0

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- AMD Am386 (1991) by AMD: AMD's 386 clone, 40 MHz (faster than Intel's 33 MHz)
- Key features: 386-compatible, 40 MHz, No on-chip cache
- Bottleneck: no_cache

**Final state:**
- CPI: 4.0 (target)
- Validation: PASSED

---
