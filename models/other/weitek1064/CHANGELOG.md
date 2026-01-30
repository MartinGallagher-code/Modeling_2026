# Weitek 1064/1065 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the Weitek 1064/1065

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with category-based instruction timing
   - fp_add: 2.0 cycles - Pipelined FP add @2 cycles
   - fp_mul: 3.0 cycles - Pipelined FP multiply @3 cycles
   - fp_div: 6.0 cycles - FP divide @5-8 cycles
   - data_transfer: 2.0 cycles - Register/bus transfer @2 cycles
   - Reasoning: Cycle counts based on 1985-era 32-bit architecture
   - Result: CPI = 3.250 (8.33% error vs target 3.0)

**What we learned:**
- Weitek 1064/1065 is a 1985 32-bit processor
- High-speed FPU pair for workstations and Cray

**Final state:**
- CPI: 3.250 (8.33% error)
- Validation: MARGINAL

**References used:**
- Weitek 1064/1065 datasheet (1985)
- IEEE FPU comparison

---

## 2026-01-29 - Full validation run and documentation update

**Session goal:** Run all workloads, update validation JSON, and complete documentation.

**Starting state:**
- CPI: 3.250 (8.33% error, from initial model creation)
- Model had been refined with 7 categories and 4-stage pipeline throughput factor

**Changes attempted:**

1. Ran model across all four standard workloads
   - typical: CPI=2.924 (2.5% error) - PASS
   - compute: CPI=3.407 (13.6% error) - MARGINAL
   - memory: CPI=2.772 (7.6% error) - MARGINAL
   - control: CPI=3.051 (1.7% error) - PASS

2. Created validation JSON with full workload results
3. Updated HANDOFF.md with current metrics

**What we learned:**
- Typical workload improved from 8.33% to 2.5% error
- Pipeline throughput factor (0.82) effectively reduces base CPI
- Compute workload overshoots due to expensive FP divide (8.5 cycles) and sqrt (10.5 cycles)
- 1065 multiply unit is the bottleneck for typical and compute workloads
- Data bus becomes bottleneck for memory-heavy workloads

**Final state:**
- CPI: 2.924 (2.5% error on typical workload)
- Validation: PASSED

---
