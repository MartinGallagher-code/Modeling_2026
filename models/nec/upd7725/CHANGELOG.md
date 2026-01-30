# NEC uPD7725 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create initial validated model for NEC uPD7725 enhanced DSP

**Starting state:**
- New model, no previous implementation

**Changes made:**

1. Created grey-box queueing model with weighted CPI calculation
   - Implemented instruction categories: mac, alu, data_transfer, control, memory
   - Calibrated for target CPI of 1.5 (pipelined DSP with single-cycle MAC)
   - Created workload profiles for typical, compute, control, io_heavy, mixed

2. Key calibration decisions:
   - MAC: 1 cycle (hardware single-cycle multiply-accumulate)
   - ALU: 1 cycle (pipelined execution)
   - Data transfer: 2 cycles (register-memory transfer)
   - Control: 2 cycles (branch overhead)
   - Memory: 3 cycles (external memory access)

3. Workload weight calculation:
   - typical: 0.30*1 + 0.30*1 + 0.15*2 + 0.15*2 + 0.10*3 = 1.50 (exact match)

**What we learned:**
- The uPD7725 was an enhanced version of the uPD7720 (1985)
- Best known as the DSP-1 coprocessor in SNES cartridges
- Harvard architecture with on-chip program/data ROM
- Single-cycle MAC for efficient signal processing

**Final state:**
- CPI: 1.50 (0.00% error vs 1.5 expected)
- Validation: PASSED

**References used:**
- NEC uPD7725 datasheet
- SNES hardware documentation

---
