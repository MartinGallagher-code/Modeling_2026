# iWarp Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the iWarp

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with category-based instruction timing
   - alu: 1.0 cycles - Single-cycle ALU (VLIW) @1 cycle
   - fp: 2.0 cycles - Pipelined FP @2 cycles throughput
   - memory: 2.0 cycles - On-chip memory @2 cycles
   - communication: 2.0 cycles - Systolic link @2 cycles
   - control: 2.0 cycles - VLIW sequencing @2 cycles
   - Reasoning: Cycle counts based on 1985-era 32-bit architecture
   - Result: CPI = 1.800 (20.00% error vs target 1.5)

**What we learned:**
- iWarp is a 1985 32-bit processor
- VLIW/systolic array processor, precursor to modern GPU thinking

**Final state:**
- CPI: 1.800 (20.00% error)
- Validation: MARGINAL

**References used:**
- iWarp architecture paper (Intel/CMU)
- Systolic array reference

---

## 2026-01-29 - Validation with updated model

**Session goal:** Run full validation of the updated iWarp model.

**Starting state:**
- CPI: 1.800 (20.00% error from initial creation)
- Model had been significantly updated with dual-issue modeling, memory miss penalties, and queueing

**Changes attempted:**

1. Ran model across all four standard workloads
   - typical: CPI=1.508, IPC=0.6631, IPS=13,262,599
   - compute: CPI=1.591, IPC=0.6287, IPS=12,573,081
   - memory: CPI=1.698, IPC=0.5891, IPS=11,782,032
   - control: CPI=1.429, IPC=0.6996, IPS=13,991,885

2. Created validation JSON with full workload results

**What we learned:**
- Updated model uses 7 categories: alu_int(1c), multiply(3c), fp_add(2c), fp_mul(3c), load_store(1c), branch(1c), comm(2c)
- Dual-issue with 80% efficiency gives effective width of 1.80
- SRAM hit rate 85%, external memory penalty 8 cycles
- Branch penalty 3 cycles at 50% mispredict rate
- Communication overhead 2 cycles at 30% rate
- Queueing factor 15% when utilization > 50%
- CPI improved dramatically from 1.800 to 1.508 (0.5% error vs 20.00%)
- Memory workload highest CPI (1.698) due to external memory misses

**Final state:**
- CPI: 1.508 (0.5% error)
- Validation: PASSED

**References used:**
- Model source: iwarp_validated.py

---
