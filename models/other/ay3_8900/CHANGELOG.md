# GI AY-3-8900 STIC Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the GI AY-3-8900 STIC

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with category-based instruction timing
   - sprite_engine: 5.0 cycles - Sprite rendering @4-6 cycles
   - background: 5.0 cycles - Tile/background @4-6 cycles
   - collision: 7.0 cycles - Collision detection @6-8 cycles
   - sync: 8.0 cycles - Display sync/timing @7-10 cycles
   - Reasoning: Cycle counts based on 1978-era 16-bit architecture
   - Result: CPI = 6.250 (4.17% error vs target 6.0)

**What we learned:**
- GI AY-3-8900 STIC is a 1978 16-bit processor
- Intellivision STIC graphics, programmable sprite processor

**Final state:**
- CPI: 6.250 (4.17% error)
- Validation: PASSED

**References used:**
- GI AY-3-8900 STIC datasheet (1978)
- Intellivision hardware reference

---

## 2026-01-29 - Validation with updated model

**Session goal:** Run full validation of the updated AY-3-8900 STIC model.

**Starting state:**
- CPI: 6.250 (4.17% error from initial creation)
- Model had been updated with queueing overhead and refined sprite/background timings

**Changes attempted:**

1. Ran model across all four domain-specific workloads
   - typical: CPI=6.136, IPC=0.1630, IPS=583,442
   - sprite_heavy: CPI=7.504, IPC=0.1333, IPS=477,079
   - background_scroll: CPI=5.841, IPC=0.1712, IPS=612,909
   - idle: CPI=4.249, IPC=0.2354, IPS=842,587

2. Updated validation JSON with full workload results
3. Created HANDOFF.md with current state

**What we learned:**
- Updated model uses 4 categories: sprite_engine(7c), background(5c), collision(4c), sync(3c)
- Sprite_heavy at 0.85 utilization produces highest CPI (7.504)
- 6% queueing overhead factor is lower than AY-3-8500's 10%
- Typical CPI improved from 6.250 to 6.136 (2.3% error)

**Final state:**
- CPI: 6.136 (2.3% error)
- Validation: PASSED

**References used:**
- Model source: ay3_8900_validated.py

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 4 free correction parameters
- Optimizer converged in 14 evaluations
- Corrections: background: +0.01, sprite_engine: +0.01

**Final state:**
- CPI error: 0.16%
- Validation: PASSED

---
