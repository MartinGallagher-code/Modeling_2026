# Intel 80C186 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial validation and documentation

**Session goal:** Validate the Intel 80C186 grey-box queueing model and create documentation.

**Starting state:**
- CPI: 5.943 (0.9% error vs target 6.0)
- Key issues: None - model was already well-calibrated

**Changes attempted:**

1. Ran model across all four workloads
   - typical: CPI=5.943, IPC=0.168, IPS=1,346,078, bottleneck=prefetch_queue
   - compute: CPI=7.167, IPC=0.140, IPS=1,116,292, bottleneck=prefetch_queue
   - memory: CPI=7.737, IPC=0.129, IPS=1,033,937, bottleneck=prefetch_queue
   - control: CPI=7.364, IPC=0.136, IPS=1,086,354, bottleneck=prefetch_queue
   - Result: Typical workload is 0.9% from target CPI of 6.0

**What we learned:**
- The 80C186 is a CMOS version of the 80186 with identical instruction timing
- Instruction categories range from 2 cycles (data_transfer) to 25 cycles (multiply/divide)
- Memory operations are 8 cycles total (4 base + 4 memory) reflecting 16-bit bus with wait states
- Memory stall calculation uses 85% factor on memory fraction plus bus queueing overhead
- Prefetch queue (6 bytes) is always the bottleneck at 0.70 utilization
- Compute and memory workloads have higher CPI than typical due to multiply/memory weight

**Final state:**
- CPI: 5.943 (0.9% error)
- Validation: PASSED

**References used:**
- Intel 80186/80C186 datasheet instruction timing tables

---
