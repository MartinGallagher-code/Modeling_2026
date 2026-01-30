# Elbrus El-90 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for Elbrus El-90

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: alu (1.0 cyc), load (2.0 cyc), store (2.0 cyc), branch (2.0 cyc), multiply (4.0 cyc), divide (15.0 cyc)
   - Architecture: Soviet superscalar design, VLIW-like
   - Target CPI: 1.5

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- Elbrus El-90 (1990) by MCST: Soviet superscalar design, VLIW-like
- Key features: VLIW-like, Soviet design, Superscalar
- Bottleneck: vliw_schedule

**Final state:**
- CPI: 1.5 (target)
- Validation: PASSED

---
