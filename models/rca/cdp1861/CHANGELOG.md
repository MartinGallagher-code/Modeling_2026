# RCA CDP1861 Pixie Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Validation pass and documentation update

**Session goal:** Validate the updated CDP1861 grey-box queueing model and complete documentation.

**Starting state:**
- Model had been significantly updated from the initial version (see entry below)
- CPI previously 5.250 with 34.38% error
- Model now has 6 categories (dma_fetch, display_active, horizontal_blank, vertical_blank, sync, interrupt)
- DMA contention modeled via M/M/1 queueing
- Validation JSON and README already existed with current results

**Changes attempted:**

1. Ran model across all four workloads to verify results
   - typical: CPI=8.229, IPC=0.122, IPS=213,987, bottleneck=sync_generator
   - compute: CPI=12.669, IPC=0.079, IPS=138,987, bottleneck=sync_generator
   - memory: CPI=5.956, IPC=0.168, IPS=295,645, bottleneck=dma_controller
   - control: CPI=9.945, IPC=0.101, IPS=177,067, bottleneck=sync_generator

2. Updated HANDOFF.md with current state
3. Created this CHANGELOG entry

**What we learned:**
- The updated model with 6 categories and DMA contention modeling is much more accurate
- vertical_blank (17 cycles) and interrupt (16 cycles) categories drive CPI up significantly
- Sync generator is the primary bottleneck for most workloads due to +0.30 base utilization
- DMA contention formula: dma_fraction / (1 - dma_fraction) * 0.15
- "compute" workload (display blanked) has highest CPI (12.669) because vertical_blank dominates
- "memory" workload (full-screen display) has lowest CPI (5.956) with dma_controller as bottleneck

**Final state:**
- CPI: 8.229 (2.9% error vs 8.0 target)
- Validation: PASSED

**References used:**
- RCA CDP1861 Pixie datasheet
- COSMAC VIP technical documentation
- Existing validation JSON and README

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the RCA CDP1861 Pixie

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with category-based instruction timing
   - dma_fetch: 6.0 cycles - DMA line fetch from 1802 @5-8 cycles
   - display_active: 8.0 cycles - Active display line @6-10 cycles
   - blanking: 4.0 cycles - Horizontal blanking @3-5 cycles
   - sync: 3.0 cycles - H/V sync generation @2-4 cycles
   - Reasoning: Cycle counts based on 1976-era 8-bit architecture
   - Result: CPI = 5.250 (34.38% error vs target 8.0)

**What we learned:**
- RCA CDP1861 Pixie is a 1976 8-bit microcontroller/processor
- Video display controller for COSMAC, used in CHIP-8 systems

**Final state:**
- CPI: 5.250 (34.38% error)
- Validation: MARGINAL

**References used:**
- RCA CDP1861 datasheet (1976)
- COSMAC VIP hardware reference

---
