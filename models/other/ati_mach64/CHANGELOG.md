# ATI Mach64 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for ATI Mach64

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: draw (2.0 cyc), pixel (1.0 cyc), register (1.0 cyc), memory (2.0 cyc), branch (3.0 cyc), blit (1.0 cyc)
   - Architecture: Hardware video playback, foundation for Rage line
   - Target CPI: 1.5

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- ATI Mach64 (1994) by ATI: Hardware video playback, foundation for Rage line
- Key features: Video playback, 2D + video, PCI bus master
- Bottleneck: pixel_throughput

**Final state:**
- CPI: 1.5 (target)
- Validation: PASSED

---
