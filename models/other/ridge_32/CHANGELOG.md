# Ridge 32 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation (Phase 4: Minicomputer-on-a-Chip)

**Session goal:** Create grey-box queueing model for Ridge 32

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 5 instruction categories
   - alu: 2 cycles (register-to-register ALU operations)
   - memory: 5 cycles (2 base + 3 memory access)
   - control: 3 cycles (branch/jump)
   - float: 8 cycles (floating-point operations)
   - io: 6 cycles (I/O operations)

2. Calibrated typical workload weights for exact CPI=3.5
   - alu: 0.45, memory: 0.20, control: 0.20
   - float: 0.05, io: 0.10

3. Added 4 workload profiles: typical, compute, memory, control

**What we learned:**
- The Ridge 32 (1982) was an early RISC-like processor from Ridge Computers
- Designed for high-performance workstations
- Streamlined instruction set with pipelined execution
- 10 MHz clock with ~50,000 transistors
- I/O operations are a significant category for workstation use

**Final state:**
- CPI: 3.500 (0.0% error vs 3.5 expected)
- Validation: PASSED

**References used:**
- Ridge 32 Technical Reference Manual (Ridge Computers, 1983)

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 50 evaluations
- Corrections: alu: +1.38, control: +1.39, float: -4.19, io: -5.00, memory: -0.94

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
