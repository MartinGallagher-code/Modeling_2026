# IIT AGX Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for IIT AGX

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: draw (2.0 cyc), pixel (2.0 cyc), register (1.0 cyc), memory (2.0 cyc), branch (3.0 cyc), blit (2.0 cyc)
   - Architecture: XGA-compatible graphics accelerator
   - Target CPI: 2.2

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- IIT AGX (1993) by IIT: XGA-compatible graphics accelerator
- Key features: XGA compatible, GUI acceleration, VRAM support
- Bottleneck: pixel_throughput

**Final state:**
- CPI: 2.2 (target)
- Validation: PASSED

---
