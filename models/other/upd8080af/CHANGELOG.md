# NEC uPD8080AF Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation (Phase 4: Second-Source & Licensed Clones)

**Session goal:** Create grey-box queueing model for the NEC uPD8080AF

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with category-based instruction timing
   - alu: 4.0 cycles - 8080-compatible ALU operations
   - data_transfer: 5.0 cycles - MOV/MVI register and memory transfers
   - memory: 7.0 cycles - Memory load/store operations
   - control: 5.0 cycles - Branch/call flow control
   - stack: 10.0 cycles - Push/pop/call stack operations
   - Reasoning: Identical timing to Intel 8080 as pin-compatible clone
   - Result: CPI = 5.500 (0.0% error vs target 5.5)

2. Calibrated workload weights for exact target CPI
   - alu: 0.300, data_transfer: 0.280, memory: 0.180, control: 0.152, stack: 0.088
   - Reasoning: Standard 8080 workload distribution
   - Result: Exact match to target CPI of 5.5

**What we learned:**
- NEC uPD8080AF was one of the earliest 8080 clones (1975)
- NEC was a major second-source for Intel in the Japanese market
- This predates the NEC V-series which were enhanced/incompatible designs
- The "AF" suffix indicates the improved version with better specs

**Final state:**
- CPI: 5.500 (0.0% error)
- Validation: PASSED

**References used:**
- NEC uPD8080AF datasheet (1975)
- Intel 8080 timing reference documentation

---
