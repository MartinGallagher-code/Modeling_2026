# Analog Devices ADSP-21020 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for Analog Devices ADSP-21020

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: mac (1.0 cyc), alu (1.0 cyc), load (1.0 cyc), store (1.0 cyc), branch (1.0 cyc), special (2.0 cyc)
   - Architecture: 32-bit floating-point SHARC predecessor
   - Target CPI: 1.2

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- Analog Devices ADSP-21020 (1990) by Analog Devices: 32-bit floating-point SHARC predecessor
- Key features: IEEE float, SHARC predecessor, Multi-function
- Bottleneck: memory_bandwidth

**Final state:**
- CPI: 1.2 (target)
- Validation: PASSED

---
