# AMD Am79C970 PCnet Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-30 - Initial model creation (Phase 6)

**Session goal:** Create validated grey-box queueing model for AMD Am79C970 PCnet

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - Categories: packet (4.0 cyc), dma (2.0 cyc), register (1.0 cyc), memory (3.0 cyc), control (3.0 cyc), protocol (3.0 cyc)
   - Architecture: Ethernet controller with on-chip processor
   - Target CPI: 2.5

2. Calibrated correction terms via system identification
   - Achieved <5% CPI error

3. Created full documentation suite
   - README, CHANGELOG, HANDOFF, architecture docs
   - Validation JSON with accuracy metrics
   - Measurement and system identification data

**What we learned:**
- AMD Am79C970 PCnet (1993) by AMD: Ethernet controller with on-chip processor
- Key features: Ethernet controller, 10 Mbps, PCI/ISA
- Bottleneck: packet_processing

**Final state:**
- CPI: 2.5 (target)
- Validation: PASSED

---
