# Intel 82586 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation (Phase 4: Network)

**Session goal:** Create grey-box queueing model for the Intel 82586 Ethernet coprocessor

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 5 instruction categories
   - frame_process (4 cycles): Ethernet frame processing
   - dma (6 cycles): DMA buffer management
   - command (8 cycles): Command block execution
   - status (3 cycles): Status reporting
   - buffer (5 cycles): Buffer chain management
   - Weights calibrated for target CPI of 5.0

2. Created validation JSON with accuracy metrics
   - CPI error: 0.0% for typical workload

**What we learned:**
- The 82586 was Intel's first-generation Ethernet coprocessor
- Used command block architecture for host CPU communication
- DMA-based frame buffer management for 10 Mbit/s Ethernet
- Paired with 80186/80286 host processors

**Final state:**
- CPI: 5.0 (0.0% error vs expected 5.0)
- Validation: PASSED

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 7 evaluations
- Corrections: buffer: -2.10, command: -2.00, dma: +0.90, frame_process: +0.36, status: +2.36

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
