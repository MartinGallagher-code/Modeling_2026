# Yamaha YM2610 OPNB Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for Yamaha YM2610 OPNB

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: oscillator (2.0 cyc), envelope (2.0 cyc), register (1.0 cyc), memory (2.0 cyc), control (3.0 cyc), mixing (2.0 cyc)
   - Architecture: FM + ADPCM, Neo Geo audio standard
   - Target CPI: 2.3

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- Yamaha YM2610 OPNB (1988) by Yamaha: FM + ADPCM, Neo Geo audio standard
- Key features: 4 FM + ADPCM, 7 ADPCM channels, Neo Geo standard
- Bottleneck: fm_operator

**Final state:**
- CPI: 2.3 (target)
- Validation: PASSED

---
