# Sony CXD8530BQ Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for Sony CXD8530BQ

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: alu (1.0 cyc), load (2.0 cyc), store (2.0 cyc), branch (2.0 cyc), multiply (4.0 cyc), divide (12.0 cyc)
   - Architecture: PlayStation CPU, MIPS R3000A with GTE coprocessor
   - Target CPI: 1.4

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- Sony CXD8530BQ (1994) by Sony/LSI Logic: PlayStation CPU, MIPS R3000A with GTE coprocessor
- Key features: MIPS R3000A core, GTE coprocessor, 4KB I+D cache
- Bottleneck: pipeline_stall

**Final state:**
- CPI: 1.4 (target)
- Validation: PASSED

---
