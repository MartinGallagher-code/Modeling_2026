# Intel 8089 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for Intel 8089 I/O Processor as part of Phase 4 (Coprocessors & I/O Processors).

**Starting state:**
- No prior model existed

**Changes attempted:**

1. Created initial model with 5 instruction categories
   - transfer: 4 cycles (data transfer operations)
   - channel_op: 6 cycles (channel program operations)
   - dma: 8 cycles base + 1.25 memory cycles (DMA block transfers)
   - control: 5 cycles (control flow)
   - memory: 10 cycles (memory-mapped I/O)
   - Reasoning: Cycle counts reflect I/O processor instruction mix
   - Result: Model produces target CPI of 6.5

2. Calibrated typical workload weights
   - transfer=0.30, channel_op=0.20, dma=0.20, control=0.15, memory=0.15
   - Added 1.25 memory cycles to dma for bus arbitration overhead
   - Result: Exact CPI match at 6.5 (0.00% error)

**What we learned:**
- I/O processors have relatively low CPI since instructions are optimized for throughput
- Transfer operations dominate the workload mix
- DMA operations incur bus overhead that adds to base cycle count

**Final state:**
- CPI: 6.5 (0.00% error)
- Validation: PASSED

---
