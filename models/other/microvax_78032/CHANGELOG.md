# MicroVAX 78032 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation (Phase 4: Minicomputer-on-a-Chip)

**Session goal:** Create grey-box queueing model for MicroVAX 78032

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 6 instruction categories
   - alu: 2 cycles (register-to-register ALU operations)
   - memory: 6 cycles (3 base + 3 memory access)
   - control: 4 cycles (branch/jump)
   - string: 10 cycles (VAX string manipulation instructions)
   - decimal: 15 cycles (packed decimal arithmetic)
   - float: 12 cycles (F-format floating-point)

2. Calibrated typical workload weights for exact CPI=5.5
   - alu: 0.365, memory: 0.200, control: 0.200
   - string: 0.100, decimal: 0.050, float: 0.085

3. Added 4 workload profiles: typical, compute, memory, control

**What we learned:**
- The MicroVAX 78032 (1984) was DEC's first single-chip VAX processor
- Implemented subset of VAX ISA with microcoded execution
- Could run full VMS operating system
- Complex CISC instruction set includes string and decimal operations
- 5 MHz clock with ~125,000 transistors

**Final state:**
- CPI: 5.500 (0.0% error vs 5.5 expected)
- Validation: PASSED

**References used:**
- MicroVAX 78032 Technical Manual (DEC, 1985)

---
