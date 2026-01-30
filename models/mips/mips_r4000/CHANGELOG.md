# MIPS R4000 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for MIPS R4000

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: alu (1.0 cyc), load (2.0 cyc), store (2.0 cyc), branch (3.0 cyc), multiply (5.0 cyc), divide (15.0 cyc)
   - Architecture: First commercial 64-bit RISC, 8-stage superpipeline
   - Target CPI: 1.5

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- MIPS R4000 (1991) by MIPS: First commercial 64-bit RISC, 8-stage superpipeline
- Key features: 8-stage superpipeline, 64-bit, On-chip caches
- Bottleneck: superpipeline_hazard

**Final state:**
- CPI: 1.5 (target)
- Validation: PASSED

---
