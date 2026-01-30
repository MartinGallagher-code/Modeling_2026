# Tseng Labs ET4000 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for Tseng Labs ET4000

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: draw (3.0 cyc), pixel (2.0 cyc), register (1.0 cyc), memory (2.0 cyc), branch (3.0 cyc), blit (2.0 cyc)
   - Architecture: Fast SVGA with hardware acceleration
   - Target CPI: 2.5

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- Tseng Labs ET4000 (1989) by Tseng Labs: Fast SVGA with hardware acceleration
- Key features: SVGA controller, Hardware acceleration, ISA/VLB
- Bottleneck: bus_bandwidth

**Final state:**
- CPI: 2.5 (target)
- Validation: PASSED

---
