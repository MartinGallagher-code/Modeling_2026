# Sequoia S-16 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation (Phase 4: Minicomputer-on-a-Chip)

**Session goal:** Create grey-box queueing model for Sequoia S-16

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 5 instruction categories
   - alu: 3 cycles (register-to-register ALU operations)
   - memory: 6 cycles (3 base + 3 memory access)
   - control: 4 cycles (branch/jump)
   - compare_swap: 8 cycles (atomic compare-and-swap for transactional integrity)
   - checkpoint: 12 cycles (hardware checkpoint/recovery operations)

2. Calibrated typical workload weights for CPI=5.002 (~5.0 target)
   - alu: 0.390, memory: 0.248, control: 0.200
   - compare_swap: 0.100, checkpoint: 0.062

3. Added 4 workload profiles: typical, compute, memory, control

**What we learned:**
- The Sequoia S-16 (1983) was a fault-tolerant processor from Sequoia Systems
- Featured hardware checkpoint and compare-and-swap operations
- Designed for high-reliability systems requiring transactional integrity
- 8 MHz clock with ~60,000 transistors
- Checkpoint operations are the most expensive at 12 cycles

**Final state:**
- CPI: 5.002 (0.04% error vs 5.0 expected)
- Validation: PASSED

**References used:**
- Sequoia S-16 Technical Reference Manual (Sequoia Systems, 1984)

---
