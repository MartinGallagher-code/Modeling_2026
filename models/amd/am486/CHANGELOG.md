# AMD Am486 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for AMD Am486

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: alu (1.0 cyc), data_transfer (1.0 cyc), memory (2.0 cyc), control (3.0 cyc), multiply (13.0 cyc), divide (25.0 cyc)
   - Architecture: AMD's 486 clone with write-back cache
   - Target CPI: 1.8

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- AMD Am486 (1993) by AMD: AMD's 486 clone with write-back cache
- Key features: 486-compatible, Write-back cache, 5-stage pipeline
- Bottleneck: pipeline

**Final state:**
- CPI: 1.8 (target)
- Validation: PASSED

---
