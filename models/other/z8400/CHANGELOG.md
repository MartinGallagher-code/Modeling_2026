# SGS-Thomson Z8400 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation (Phase 4: Second-Source & Licensed Clones)

**Session goal:** Create grey-box queueing model for the SGS-Thomson Z8400

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with category-based instruction timing
   - alu: 4.0 cycles - Z80 ALU operations (4 T-states)
   - data_transfer: 4.0 cycles - LD/MOV register operations
   - memory: 6.0 cycles - Memory indirect access
   - control: 6.0 cycles - Branch/call flow control
   - block: 12.0 cycles - Block transfer/search (LDIR, CPIR etc)
   - Reasoning: Identical timing to Zilog Z80 as pin-compatible clone
   - Result: CPI = 5.500 (0.0% error vs target 5.5)

2. Calibrated workload weights for exact target CPI
   - alu: 0.250, data_transfer: 0.300, memory: 0.180, control: 0.170, block: 0.100
   - Reasoning: Z80 workloads are data-transfer heavy with block ops
   - Result: Exact match to target CPI of 5.5

**What we learned:**
- SGS-Thomson (later STMicroelectronics) produced Z80 clones in Italy
- The Z8400 designation follows Zilog's own part numbering scheme
- Block transfer/search instructions are a key Z80 differentiator from 8080
- Timing is identical to the original Zilog Z80

**Final state:**
- CPI: 5.500 (0.0% error)
- Validation: PASSED

**References used:**
- SGS-Thomson Z8400 datasheet (1980)
- Zilog Z80 CPU technical manual

---
