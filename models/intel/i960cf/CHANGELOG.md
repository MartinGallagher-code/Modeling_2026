# Intel i960CF Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for Intel i960CF

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: alu (1.0 cyc), load (1.0 cyc), store (1.0 cyc), branch (1.0 cyc), multiply (2.0 cyc), divide (8.0 cyc)
   - Architecture: Enhanced i960 with on-chip FPU
   - Target CPI: 0.85

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- Intel i960CF (1992) by Intel: Enhanced i960 with on-chip FPU
- Key features: On-chip FPU, 4KB I-cache, Superscalar
- Bottleneck: issue_width

**Final state:**
- CPI: 0.85 (target)
- Validation: PASSED

---
