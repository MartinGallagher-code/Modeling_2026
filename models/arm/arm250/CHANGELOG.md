# ARM250 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for ARM250

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: alu (1.0 cyc), load (2.0 cyc), store (2.0 cyc), branch (3.0 cyc), multiply (8.0 cyc), divide (30.0 cyc)
   - Architecture: ARM2 with MMU, MEMC, VIDC integrated, Acorn A3000
   - Target CPI: 1.7

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- ARM250 (1990) by ARM/VLSI: ARM2 with MMU, MEMC, VIDC integrated, Acorn A3000
- Key features: ARM2 core, Integrated MMU+MEMC+VIDC, 26-bit address
- Bottleneck: single_issue

**Final state:**
- CPI: 1.7 (target)
- Validation: PASSED

---
