# Cypress CY7C601 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for Cypress CY7C601

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: alu (1.0 cyc), load (2.0 cyc), store (2.0 cyc), branch (2.0 cyc), multiply (5.0 cyc), divide (16.0 cyc)
   - Architecture: Early merchant SPARC, 25-40 MHz
   - Target CPI: 1.6

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- Cypress CY7C601 (1988) by Cypress: Early merchant SPARC, 25-40 MHz
- Key features: SPARC V7, FPU companion CY7C602, Early merchant SPARC
- Bottleneck: pipeline_stall

**Final state:**
- CPI: 1.6 (target)
- Validation: PASSED

---
