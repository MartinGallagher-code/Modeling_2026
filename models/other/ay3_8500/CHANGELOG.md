# GI AY-3-8500 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the GI AY-3-8500

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with category-based instruction timing
   - game_logic: 3.0 cycles - Ball/paddle computation @3 cycles
   - video_gen: 4.0 cycles - Video signal generation @4 cycles
   - sync: 4.0 cycles - H/V sync timing @4 cycles
   - io: 5.0 cycles - Paddle/switch input @5 cycles
   - Reasoning: Cycle counts based on 1976-era 1-bit architecture
   - Result: CPI = 4.000 (0.00% error vs target 4.0)

**What we learned:**
- GI AY-3-8500 is a 1976 1-bit microcontroller/processor
- Pong-on-a-chip, launched home gaming revolution

**Final state:**
- CPI: 4.000 (0.00% error)
- Validation: PASSED

**References used:**
- GI AY-3-8500 datasheet (1976)
- Pong hardware analysis

---

## 2026-01-29 - Validation with updated model

**Session goal:** Run full validation of the updated AY-3-8500 model with queueing overhead.

**Starting state:**
- CPI: 4.000 (0.00% error from initial creation)
- Model had been updated with M/M/1 queueing and refined category timings

**Changes attempted:**

1. Ran model across all four domain-specific workloads
   - typical: CPI=4.149, IPC=0.2410, IPS=482,094
   - active_play: CPI=5.040, IPC=0.1984, IPS=396,825
   - idle: CPI=3.135, IPC=0.3190, IPS=637,959
   - video_heavy: CPI=3.771, IPC=0.2652, IPS=530,303

2. Updated validation JSON with full workload results
3. Created HANDOFF.md with current state

**What we learned:**
- Updated model uses 4 categories: game_logic(4c), video_gen(3c), sync(2c), io(6c)
- Utilization varies: typical=0.72, idle=0.50, active_play=0.80
- Active play CPI (5.040) is highest due to 0.80 utilization and IO-heavy workload
- Idle is fastest (3.135) with video_gen+sync dominant at low utilization

**Final state:**
- CPI: 4.149 (3.7% error)
- Validation: PASSED

**References used:**
- Model source: ay3_8500_validated.py

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 4 free correction parameters
- Optimizer converged in 18 evaluations
- Corrections: game_logic: -0.04, io: -0.04, sync: -0.07, video_gen: -0.07

**Final state:**
- CPI error: 1.38%
- Validation: PASSED

---
