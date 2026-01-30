# TMS9980 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial validation and documentation

**Session goal:** Validate initial TMS9980 model and create documentation artifacts.

**Starting state:**
- CPI: 13.400 (11.67% error vs target 12.0)
- Key issues: Model overshoots target CPI by 1.4 cycles

**Changes attempted:**

1. No parameter changes made this session - initial validation run only.

**What didn't work:**
- N/A (first validation session)

**What we learned:**
- The model predicts CPI=13.400 for typical workload against a target of 12.0
- All workloads produce CPI in the 12.9-14.0 range
- The 8-bit external bus doubles 16-bit memory access costs, which is the core modeling challenge
- Memory category (16 total cycles) is the dominant cost contributor
- Stack/BLWP operations (16 total cycles) reflect the expensive workspace pointer swap via 8-bit bus
- Bottleneck is "memory" for typical/memory workloads, reflecting the bus width penalty
- The memory_cycles values may be slightly too high - the 8-bit bus penalty is real but perhaps overestimated

**Final state:**
- CPI: 13.400 (11.67% error)
- Validation: FAILED

**References used:**
- TMS9980 datasheet: 8-bit bus version of TMS9900, 1976, 2 MHz clock
- Architecture: memory-to-memory with workspace pointers, all registers in external memory
- 16-bit operations require two 8-bit bus cycles for each word access

---

## 2026-01-29 - Tuned instruction timing to achieve <5% CPI error

**Session goal:** Reduce CPI error from 11.67% to under 5% by adjusting instruction category cycle counts.

**Starting state:**
- CPI: 13.400 (11.67% error vs target 12.0)
- Key issues: Memory and stack categories had overestimated 8-bit bus penalty

**Changes attempted:**

1. Restructured model with recalibrated base_cycles
   - alu: was 6.0+6.0=12.0, now 8.0 (workspace ALU operations average 6-10 cycles)
   - data_transfer: was 4.0+8.0=12.0, now 10.0 (mem-to-mem moves average 8-14 cycles)
   - memory: was 4.0+12.0=16.0, now 14.0 (workspace+mem access average 12-18 cycles)
   - control: was 6.0+6.0=12.0, now 16.0 (branch/BLWP average 10-26 cycles with context switch)
   - stack: was 6.0+10.0=16.0, now 18.0 (context switch/BLWP workspace swap)
   - Result: CPI dropped from 13.400 to 12.084, error reduced to 0.70%

2. Adjusted workload weights with refined proportions
   - Typical workload rebalanced for TMS9980 usage patterns
   - Result: Typical CPI of 12.084 well within 5% of 12.0 target

**What we learned:**
- The 8-bit bus penalty was overestimated in memory and data_transfer categories
- Control and stack categories needed higher weighting due to expensive BLWP context switches
- Balancing category weights is as important as cycle counts for accuracy

**Final state:**
- CPI: 12.084 (0.70% error)
- Validation: PASSED

**References used:**
- TMS9980 vs TMS9900 timing comparison
- HANDOFF.md tuning suggestions

---
