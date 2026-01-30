# SGS-Thomson D950 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for SGS-Thomson D950

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: mac (1.0 cyc), alu (1.0 cyc), load (1.0 cyc), store (1.0 cyc), branch (2.0 cyc), special (3.0 cyc)
   - Architecture: European DSP for GSM baseband processing
   - Target CPI: 1.4

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- SGS-Thomson D950 (1991) by SGS-Thomson: European DSP for GSM baseband processing
- Key features: GSM baseband, European design, Viterbi support
- Bottleneck: mac_throughput

**Final state:**
- CPI: 1.4 (target)
- Validation: PASSED

---
