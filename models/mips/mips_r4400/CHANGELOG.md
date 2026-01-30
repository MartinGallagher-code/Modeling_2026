# MIPS R4400 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for MIPS R4400

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: alu (1.0 cyc), load (2.0 cyc), store (2.0 cyc), branch (3.0 cyc), multiply (5.0 cyc), divide (14.0 cyc)
   - Architecture: Improved R4000 with larger caches, SGI Indy/Indigo2
   - Target CPI: 1.4

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- MIPS R4400 (1993) by MIPS: Improved R4000 with larger caches, SGI Indy/Indigo2
- Key features: 8-stage superpipeline, 64-bit, Larger L1 caches
- Bottleneck: superpipeline_hazard

**Final state:**
- CPI: 1.4 (target)
- Validation: PASSED

---
