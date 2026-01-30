# Sega SVP (SSP1601) Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for Sega SVP (SSP1601)

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: mac (1.0 cyc), alu (1.0 cyc), load (1.0 cyc), store (1.0 cyc), branch (2.0 cyc), special (3.0 cyc)
   - Architecture: DSP in Virtua Racing cartridge
   - Target CPI: 1.5

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- Sega SVP (SSP1601) (1994) by Samsung: DSP in Virtua Racing cartridge
- Key features: Samsung SSP1601, 16-bit DSP, In-cartridge
- Bottleneck: mac_throughput

**Final state:**
- CPI: 1.5 (target)
- Validation: PASSED

---
