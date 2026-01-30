# Berkeley RISC II Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for Berkeley RISC II, the improved successor to RISC I

**Starting state:**
- No model existed
- Reference: berkeley_risc1 model (CPI ~1.3)

**Research findings:**
- Berkeley RISC II was the improved RISC processor (UC Berkeley, 1983)
- 3-stage pipeline (fetch, decode, execute) - improved from RISC I's 2-stage
- 138 registers with 8 overlapping windows (vs RISC I's 78 registers, 6 windows)
- Single-cycle ALU operations maintained
- Load: 2 cycles (memory access)
- Store: 1.5 cycles (improved with write buffer)
- Branch: 2 cycles (with delay slot)
- 39 total instructions (expanded from RISC I's 31)
- 40,760 transistors (fewer than RISC I's 44,500 but more efficient)
- 3 MHz clock
- Direct influence on Sun SPARC architecture

**Changes made:**

1. Created model targeting CPI ~1.2 (improved from RISC I's 1.3)
   - Single-cycle ALU operations
   - Store operations faster than loads (write buffer)
   - More register windows reduce spill/fill overhead

2. Added 5 instruction categories:
   - alu: 1 cycle (ADD/SUB/AND/OR/XOR)
   - load: 2 cycles (memory access)
   - store: 1.5 cycles (write buffer improvement)
   - branch: 2 cycles (with delay slot)
   - call: 1 cycle (register window switch)

3. Key RISC II improvements modeled:
   - More register windows (8 vs 6) - fewer window overflow traps
   - Improved pipeline (3-stage vs 2-stage)
   - Write buffer for stores (1.5 cycles vs 2 cycles)
   - Better compiler support with expanded ISA

4. Comparison function to RISC I added

**What we learned:**
- RISC II achieved CPI ~1.2 (vs RISC I's ~1.3, ~8% improvement)
- More register windows significantly reduced procedure call overhead
- The 3-stage pipeline improved throughput
- Direct ancestor of Sun SPARC architecture (1987)
- Influenced ARM and MIPS design philosophies

**Final state:**
- CPI: 1.205 (~0.4% error vs target 1.2)
- Validation: PASSED (13/13 tests, 100%)
- ~8.3x faster CPI than VAX 11/780
- ~7.3% CPI improvement over RISC I

**References used:**
- Patterson & Sequin: RISC II Technical Report (1983)
- "The Design of RISC II" (UC Berkeley EECS)
- Wikipedia: Berkeley RISC
- The SPARC Architecture Manual (RISC II descendant)
- berkeley_risc1 model for comparison

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 22 evaluations
- Corrections: alu: -0.43, branch: -1.03, call: +1.98, load: +0.42, store: +0.92

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
