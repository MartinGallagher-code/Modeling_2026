# Clipper C100 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation (Phase 4: Minicomputer-on-a-Chip)

**Session goal:** Create grey-box queueing model for Fairchild Clipper C100

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 5 instruction categories
   - alu: 1 cycle (register-to-register ALU operations)
   - load: 2 cycles (load from memory/cache)
   - store: 1 cycle (store to memory/cache)
   - branch: 2 cycles (branch/jump)
   - float: 3 cycles (floating-point operations)

2. Calibrated typical workload weights for exact CPI=1.5
   - alu: 0.400, load: 0.200, store: 0.175
   - branch: 0.150, float: 0.075

3. Added 4 workload profiles: typical, compute, memory, control

**What we learned:**
- The Clipper C100 (1985) was Fairchild's RISC processor
- Featured separate instruction and data caches
- Load/store architecture with pipelined execution
- 33 MHz clock with ~132,000 transistors
- Achieved high throughput with single-cycle ALU and store operations

**Final state:**
- CPI: 1.500 (0.0% error vs 1.5 expected)
- Validation: PASSED

**References used:**
- Clipper C100 Technical Reference Manual (Fairchild, 1986)

---

## 2026-01-29 - System identification (rolled back)

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Result:** Optimization was rolled back because it worsened typical-workload error.
- 5 free correction parameters
- Structural mismatch between workload profiles and measurements
- Model left unchanged

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
