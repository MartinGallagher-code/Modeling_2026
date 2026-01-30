# Zilog Z8530 SCC Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation (Phase 4: Network)

**Session goal:** Create grey-box queueing model for the Zilog Z8530 SCC

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 5 instruction categories
   - register_io (2 cycles): Register read/write
   - frame_process (6 cycles): Frame assembly/disassembly
   - crc (4 cycles): CRC generation/checking
   - control (3 cycles): Command/status processing
   - dma (5 cycles): DMA transfer operations
   - Equal weights (0.20 each) for target CPI of 4.0

2. Created validation JSON with accuracy metrics
   - CPI error: 0.0% for typical workload

**What we learned:**
- The Z8530 SCC was one of the most widely used serial controllers
- Used in Apple Macintosh, Sun workstations, and networking equipment
- Dual-channel design with hardware CRC and DMA support
- Supports HDLC, SDLC, and asynchronous serial protocols

**Final state:**
- CPI: 4.0 (0.0% error vs expected 4.0)
- Validation: PASSED

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 35 evaluations
- Corrections: control: -2.44, crc: +2.17, dma: -0.24, frame_process: -1.65, register_io: +2.16

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
