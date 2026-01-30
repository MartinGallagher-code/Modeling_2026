# NEC V810 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for NEC V810

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: alu (1.0 cyc), load (2.0 cyc), store (2.0 cyc), branch (2.0 cyc), multiply (5.0 cyc), divide (15.0 cyc)
   - Architecture: 32-bit RISC, 5-stage pipeline, Virtual Boy/PC-FX
   - Target CPI: 1.5

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- NEC V810 (1993) by NEC: 32-bit RISC, 5-stage pipeline, Virtual Boy/PC-FX
- Key features: 5-stage pipeline, 1KB I-cache, 32 GPRs
- Bottleneck: pipeline_stall

**Final state:**
- CPI: 1.5 (target)
- Validation: PASSED

---
