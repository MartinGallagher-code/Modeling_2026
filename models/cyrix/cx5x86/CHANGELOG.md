# Cyrix Cx5x86 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for Cyrix Cx5x86

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: alu (1.0 cyc), data_transfer (1.0 cyc), memory (2.0 cyc), control (3.0 cyc), multiply (6.0 cyc), divide (18.0 cyc)
   - Architecture: Superscalar 486-socket chip, bridge to 6x86
   - Target CPI: 1.5

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- Cyrix Cx5x86 (1995) by Cyrix: Superscalar 486-socket chip, bridge to 6x86
- Key features: Superscalar, 16KB unified cache, 486 socket
- Bottleneck: pipeline

**Final state:**
- CPI: 1.5 (target)
- Validation: PASSED

---
