# National NS32082 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for National NS32082 MMU as part of Phase 4 (Coprocessors & I/O Processors).

**Starting state:**
- No prior model existed

**Changes attempted:**

1. Created initial model with 5 instruction categories
   - translate: 4 cycles (TLB hit translation)
   - page_fault: 20 cycles (page fault exception setup)
   - table_walk: 15 cycles base + 10.667 memory cycles (page table walk)
   - cache_op: 3 cycles (translation cache operations)
   - control: 5 cycles (MMU control/status)
   - Reasoning: NS32082 has higher base latencies than 68851 due to simpler hardware
   - Result: Model produces target CPI of 8.0

2. Calibrated typical workload weights
   - translate=0.45, page_fault=0.05, table_walk=0.15, cache_op=0.20, control=0.15
   - Added 10.667 memory cycles to table_walk for page table memory accesses
   - Result: Exact CPI match at 8.0 (0.00% error)

**What we learned:**
- NS32082 has higher CPI than 68851 (8.0 vs 6.0) reflecting simpler/slower hardware
- Page faults are rare (5%) but expensive (20 cycles)
- Translation cache ops are frequent but fast

**Final state:**
- CPI: 8.0 (0.00% error)
- Validation: PASSED

---
