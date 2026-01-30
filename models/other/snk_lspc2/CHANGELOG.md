# SNK LSPC2-A2 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for SNK LSPC2-A2

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: draw (2.0 cyc), pixel (2.0 cyc), register (1.0 cyc), memory (3.0 cyc), branch (4.0 cyc), blit (2.0 cyc)
   - Architecture: Neo Geo video processor, hardware sprite scaler
   - Target CPI: 2.5

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- SNK LSPC2-A2 (1990) by SNK: Neo Geo video processor, hardware sprite scaler
- Key features: 380 sprites on screen, Hardware scaling, Arcade standard
- Bottleneck: sprite_engine

**Final state:**
- CPI: 2.5 (target)
- Validation: PASSED

---
