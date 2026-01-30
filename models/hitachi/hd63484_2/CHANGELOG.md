# Hitachi HD63484-2 ACRTC Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for Hitachi HD63484-2 ACRTC

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: draw (3.0 cyc), pixel (3.0 cyc), register (1.0 cyc), memory (3.0 cyc), branch (4.0 cyc), blit (3.0 cyc)
   - Architecture: Enhanced ACRTC, faster drawing commands
   - Target CPI: 3.5

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- Hitachi HD63484-2 ACRTC (1987) by Hitachi: Enhanced ACRTC, faster drawing commands
- Key features: Enhanced ACRTC, Hardware drawing, Faster fill
- Bottleneck: drawing_engine

**Final state:**
- CPI: 3.5 (target)
- Validation: PASSED

---
