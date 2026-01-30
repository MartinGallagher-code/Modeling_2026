# ATI Mach32 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for ATI Mach32

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: draw (2.0 cyc), pixel (2.0 cyc), register (1.0 cyc), memory (2.0 cyc), branch (3.0 cyc), blit (1.0 cyc)
   - Architecture: ATI's first true graphics coprocessor
   - Target CPI: 1.8

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- ATI Mach32 (1992) by ATI: ATI's first true graphics coprocessor
- Key features: GUI acceleration, Hardware cursor, PCI support
- Bottleneck: pixel_throughput

**Final state:**
- CPI: 1.8 (target)
- Validation: PASSED

---
