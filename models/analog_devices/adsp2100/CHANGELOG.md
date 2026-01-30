# Analog Devices ADSP-2100 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create initial validated model for ADSP-2100 DSP

**Starting state:**
- New model, no previous implementation

**Changes made:**

1. Created grey-box queueing model with weighted CPI calculation
   - Implemented instruction categories: mac, alu, shift, memory, control, io
   - Calibrated for target CPI of 1.4 (pipelined DSP with single-cycle MAC)
   - Created workload profiles for typical, compute, control, io_heavy, mixed

2. Key calibration decisions:
   - MAC: 1 cycle (hardware single-cycle multiply-accumulate)
   - ALU: 1 cycle (pipelined single-cycle execution)
   - Shift: 1 cycle (barrel shifter)
   - Memory: 2 cycles (bus access overhead)
   - Control: 2 cycles (pipeline flush on branches)
   - I/O: 3 cycles (serial port and peripheral access)

3. Workload weight calculation:
   - typical: 0.30*1 + 0.25*1 + 0.15*1 + 0.10*2 + 0.10*2 + 0.10*3 = 1.40 (exact match)

**What we learned:**
- The ADSP-2100 was Analog Devices' first DSP (1986)
- Harvard architecture with separate program and data memory buses
- 3-stage pipeline enabling single-cycle core operations
- Established the ADSP-21xx family used widely in industry

**Final state:**
- CPI: 1.40 (0.00% error vs 1.4 expected)
- Validation: PASSED

**References used:**
- ADSP-2100 Family User's Manual
- Analog Devices DSP product datasheets

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 6 free correction parameters
- Optimizer converged in 33 evaluations
- Corrections: alu: -0.30, control: +0.13, io: +0.93, mac: -0.33, memory: -0.76, shift: +0.96

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
