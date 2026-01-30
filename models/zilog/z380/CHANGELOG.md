# Zilog Z380 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for Zilog Z380

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: alu (2.0 cyc), data_transfer (2.0 cyc), memory (4.0 cyc), control (6.0 cyc), multiply (14.0 cyc), divide (30.0 cyc)
   - Architecture: 32-bit Z80 extension, Z80 compatibility
   - Target CPI: 3.0

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- Zilog Z380 (1994) by Zilog: 32-bit Z80 extension, Z80 compatibility
- Key features: Z80 compatible, 32-bit extensions, Embedded/telecom
- Bottleneck: bus_contention

**Final state:**
- CPI: 3.0 (target)
- Validation: PASSED

---
