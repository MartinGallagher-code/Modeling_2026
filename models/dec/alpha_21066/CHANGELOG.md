# DEC Alpha 21066 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for DEC Alpha 21066

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: alu (1.0 cyc), load (2.0 cyc), store (2.0 cyc), branch (2.0 cyc), multiply (4.0 cyc), divide (15.0 cyc)
   - Architecture: Low-cost Alpha with integrated PCI/memory controller
   - Target CPI: 1.3

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- DEC Alpha 21066 (1993) by DEC: Low-cost Alpha with integrated PCI/memory controller
- Key features: Alpha EV4 core, Integrated PCI, Low-cost Alpha PC
- Bottleneck: memory_controller

**Final state:**
- CPI: 1.3 (target)
- Validation: PASSED

---
