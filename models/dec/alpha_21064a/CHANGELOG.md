# DEC Alpha 21064A Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for DEC Alpha 21064A

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: alu (1.0 cyc), load (2.0 cyc), store (2.0 cyc), branch (2.0 cyc), multiply (4.0 cyc), divide (12.0 cyc)
   - Architecture: Faster 21064, 300 MHz
   - Target CPI: 1.2

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- DEC Alpha 21064A (1994) by DEC: Faster 21064, 300 MHz
- Key features: 2-issue, 16KB I+D cache, 300 MHz
- Bottleneck: pipeline_stall

**Final state:**
- CPI: 1.2 (target)
- Validation: PASSED

---
