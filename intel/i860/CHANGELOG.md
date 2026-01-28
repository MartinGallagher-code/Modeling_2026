# Intel i860 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-28 - Major calibration overhaul

**Session goal:** Fix model that had 150% CPI error

**Starting state:**
- CPI: 3.01 (150.8% error vs expected 1.2)
- Key issues: Model was using generic "Cache/RISC" template that didn't account for i860's unique VLIW-hybrid architecture

**Changes attempted:**

1. Fixed clock speed
   - Parameter: `clock_mhz` changed from 25.0 to 40.0
   - Reasoning: 25 MHz was low-end; 40 MHz was standard, 50 MHz was max
   - Result: Reduced CPI slightly, but not the main issue

2. Enabled delayed branch modeling
   - Parameter: `has_delayed_branch` changed from False to True
   - Added: `branch_delay_slots = 3`
   - Added: `delay_slot_fill_rate = 0.8`
   - Reasoning: i860 has 3 branch delay slots per architecture spec
   - Result: Reduced branch penalty significantly

3. Added dual-issue modeling
   - Added: `dual_issue = True`
   - Added: `dual_issue_efficiency = 0.55`
   - Reasoning: i860 can issue int AND fp instruction simultaneously (VLIW-hybrid)
   - Result: Major improvement - this was the key missing feature

4. Fixed cache configuration
   - Parameter: `dcache_size_kb` changed from 4 to 8 (per spec)
   - Parameter: `icache_hit_rate` changed from 0.95 to 0.975
   - Parameter: `dcache_hit_rate` changed from 0.9 to 0.94
   - Parameter: `memory_latency` changed from 10 to 6
   - Reasoning: Scientific workloads have good locality; 8KB D-cache per datasheet
   - Result: Reduced cache miss penalties

5. Fixed instruction timings for pipelined operations
   - Parameter: `multiply` cycles changed from 10 to 3
   - Parameter: `divide` cycles changed from 30 to 8
   - Parameter: `fp_single` cycles changed from 3 to 1
   - Parameter: `fp_double` cycles changed from 6 to 1
   - Reasoning: i860 had fully pipelined FP with 1/cycle throughput
   - Result: Reduced multi-cycle instruction penalties

6. Updated workload profiles
   - Increased FP weights (i860 was for scientific/graphics)
   - `typical` FP fraction: 8% -> 24%
   - Added `mixed` workload profile
   - Reasoning: i860 was not used for general-purpose computing
   - Result: Better reflects actual usage patterns

**What didn't work:**

- Initial attempt with `dual_issue_efficiency = 0.4` gave 8.2% error (too conservative)
- `icache_hit_rate = 0.96` still gave ~6% error (needed 0.975)
- Keeping `multiply` penalty at `weight * 1.5` was too high for pipelined multiply
- Tried `memory_latency = 8` initially - 6 worked better for 40 MHz

**What we learned:**

- The i860 was a VLIW-hybrid, NOT a standard RISC processor
- "Cray on a chip" marketing was accurate but only for hand-tuned code
- Expected CPI of 1.2 represents "reasonably optimized" code
- Peak would be CPI ~0.5 with full dual-issue utilization
- Naive compiled code would see CPI 2-3 (which original template produced)
- The processor failed commercially because compilers couldn't optimize for it
- 3 branch delay slots are unusual - most RISC had 1

**Final state:**
- CPI: 1.257 (4.8% error)
- Validation: PASSED

**References used:**
- Validation JSON expected values
- Architecture documentation in docs/ folder
- WikiChip i860 specifications

---
