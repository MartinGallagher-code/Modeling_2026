# AT&T DSP16 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for AT&T DSP16

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: mac (1.0 cyc), alu (1.0 cyc), load (1.0 cyc), store (1.0 cyc), branch (2.0 cyc), special (3.0 cyc)
   - Architecture: 16-bit fixed-point, low-power, modems/voice
   - Target CPI: 1.3

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- AT&T DSP16 (1987) by AT&T: 16-bit fixed-point, low-power, modems/voice
- Key features: 16-bit, Low power, Voice processing
- Bottleneck: mac_throughput

**Final state:**
- CPI: 1.3 (target)
- Validation: PASSED

---
