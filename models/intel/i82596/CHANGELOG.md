# Intel i82596 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for Intel i82596

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: packet (4.0 cyc), dma (3.0 cyc), register (1.0 cyc), memory (3.0 cyc), control (3.0 cyc), protocol (4.0 cyc)
   - Architecture: 32-bit Ethernet coprocessor, TCP offload
   - Target CPI: 3.0

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- Intel i82596 (1987) by Intel: 32-bit Ethernet coprocessor, TCP offload
- Key features: 32-bit LAN coprocessor, TCP offload, DMA engine
- Bottleneck: packet_processing

**Final state:**
- CPI: 3.0 (target)
- Validation: PASSED

---
