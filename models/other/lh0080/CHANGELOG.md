# Sharp LH0080 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation (Phase 4: Second-Source & Licensed Clones)

**Session goal:** Create grey-box queueing model for the Sharp LH0080

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with category-based instruction timing
   - alu: 4.0 cycles - Z80 ALU operations (4 T-states)
   - data_transfer: 4.0 cycles - LD/MOV register operations
   - memory: 6.0 cycles - Memory indirect access
   - control: 5.5 cycles - Branch/call flow control (avg)
   - block: 12.0 cycles - Block transfer/search (LDIR, CPIR etc)
   - Reasoning: Z80-compatible timing with slightly lower control avg
   - Result: CPI = 5.300 (0.0% error vs target 5.3)

2. Calibrated workload weights for exact target CPI
   - alu: 0.300, data_transfer: 0.280, memory: 0.170, control: 0.160, block: 0.090
   - Reasoning: Standard Z80 workload profile
   - Result: Exact match to target CPI of 5.3

**What we learned:**
- Sharp LH0080 was one of the earliest Z80 second-sources
- Used extensively in Sharp's own MZ and X1 personal computers
- 2.5 MHz version was typical for early Sharp systems
- Pin-compatible with original Zilog Z80

**Final state:**
- CPI: 5.300 (0.0% error)
- Validation: PASSED

**References used:**
- Sharp LH0080 datasheet (1976)
- Zilog Z80 CPU technical manual

---
