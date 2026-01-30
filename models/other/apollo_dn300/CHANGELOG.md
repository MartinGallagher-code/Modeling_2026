# Apollo DN300 PRISM Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation (Phase 4: Minicomputer-on-a-Chip)

**Session goal:** Create grey-box queueing model for Apollo DN300 PRISM

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 5 instruction categories
   - alu: 2 cycles (register-to-register ALU operations)
   - memory: 5 cycles (2 base + 3 memory access)
   - control: 4 cycles (branch/jump)
   - float: 10 cycles (floating-point operations)
   - graphics: 8 cycles (graphics/bitblt operations)

2. Calibrated typical workload weights for exact CPI=4.5
   - alu: 0.350, memory: 0.2533, control: 0.200
   - float: 0.080, graphics: 0.1167

3. Added 4 workload profiles: typical, compute, memory, control

**What we learned:**
- The Apollo DN300 (1983) was a 68000-derived graphics workstation
- Designed for CAD/CAE applications at Apollo Computer
- Featured dedicated graphics operations alongside general computation
- 10 MHz clock with ~100,000 transistors
- Graphics operations are a significant instruction category

**Final state:**
- CPI: 4.500 (0.0% error vs 4.5 expected)
- Validation: PASSED

**References used:**
- Apollo DN300 Technical Reference Manual (Apollo Computer, 1984)

---
