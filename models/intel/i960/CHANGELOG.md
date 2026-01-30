# Intel i960 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for Intel i960

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: alu (1.0 cyc), load (2.0 cyc), store (2.0 cyc), branch (2.0 cyc), multiply (3.0 cyc), divide (10.0 cyc)
   - Architecture: 32-bit embedded RISC, register scoreboarding
   - Target CPI: 1.5

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- Intel i960 (1988) by Intel: 32-bit embedded RISC, register scoreboarding
- Key features: Register scoreboarding, 32-bit RISC, Local register cache
- Bottleneck: register_scoreboard

**Final state:**
- CPI: 1.5 (target)
- Validation: PASSED

---
