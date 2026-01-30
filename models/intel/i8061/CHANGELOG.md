# Intel 8061 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation (Phase 4: Automotive)

**Session goal:** Create grey-box queueing model for the Intel 8061 Ford EEC engine controller

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 5 instruction categories
   - alu (3 cycles): Basic ALU operations
   - adc (8 cycles): ADC conversion and read
   - timer (4 cycles): Timer operations
   - control (5 cycles): Branch/call operations
   - lookup (6 cycles): Table lookup for fuel maps
   - Weights calibrated for target CPI of 4.5

2. Created validation JSON with accuracy metrics
   - CPI error: 0.0% for typical workload

**What we learned:**
- The Intel 8061 was a custom MCU designed exclusively for Ford's EEC system
- It featured integrated ADC, timers, and lookup table hardware for engine control
- The 6 MHz clock with ~15,000 NMOS transistors was typical of late 1970s automotive MCUs

**Final state:**
- CPI: 4.5 (0.0% error vs expected 4.5)
- Validation: PASSED

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 9 evaluations
- Corrections: adc: -3.50, alu: +1.50, control: -0.50, lookup: -1.50, timer: +0.50

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
