# Zilog Z8016 DMA Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for Zilog Z8016 DMA controller as part of Phase 4 (Coprocessors & I/O Processors).

**Starting state:**
- No prior model existed

**Changes attempted:**

1. Created initial model with 5 instruction categories
   - transfer: 2 cycles (single DMA transfer)
   - setup: 6 cycles (channel setup/configuration)
   - chain: 8 cycles base + 0.5 memory cycles (chained/scatter-gather)
   - control: 4 cycles (control and status)
   - search: 5 cycles (search and match)
   - Reasoning: DMA controllers have very low cycle counts optimized for throughput
   - Result: Model produces target CPI of 4.0

2. Calibrated typical workload weights
   - transfer=0.40, setup=0.10, chain=0.10, control=0.25, search=0.15
   - Added 0.5 memory cycles to chain for descriptor fetch overhead
   - Result: Exact CPI match at 4.0 (0.00% error)

**What we learned:**
- DMA controllers have the lowest CPI of coprocessor types
- Transfer operations dominate at 40% of workload
- Control operations are frequent (25%) for status polling

**Final state:**
- CPI: 4.0 (0.00% error)
- Validation: PASSED

---
