# SGI R10000 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for SGI R10000

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: alu (1.0 cyc), load (1.0 cyc), store (1.0 cyc), branch (1.0 cyc), multiply (2.0 cyc), divide (8.0 cyc)
   - Architecture: Out-of-order MIPS, register renaming
   - Target CPI: 0.6

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- SGI R10000 (1994) by MIPS/SGI: Out-of-order MIPS, register renaming
- Key features: 4-issue out-of-order, Register renaming, 32KB I+D
- Bottleneck: issue_width

**Final state:**
- CPI: 0.6 (target)
- Validation: PASSED

---
