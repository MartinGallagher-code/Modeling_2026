# Intel i960CA Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for Intel i960CA

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: alu (1.0 cyc), load (1.0 cyc), store (1.0 cyc), branch (1.0 cyc), multiply (2.0 cyc), divide (8.0 cyc)
   - Architecture: Superscalar i960, 3-issue, RAID controller standard
   - Target CPI: 0.9

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- Intel i960CA (1989) by Intel: Superscalar i960, 3-issue, RAID controller standard
- Key features: 3-issue superscalar, 1KB I-cache, Register scoreboard
- Bottleneck: issue_width

**Final state:**
- CPI: 0.9 (target)
- Validation: PASSED

---
