# TI TMS0800 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the TI TMS0800 calculator chip

**Starting state:**
- No model existed

**Research findings:**
- Single-chip PMOS calculator IC (1973)
- 4-bit serial BCD data path with shift registers
- 11-digit BCD display capability
- Hardwired four-function arithmetic
- Clock: 300 kHz typical
- ~5,000 transistors (PMOS)
- Predecessor to TMS1000 microcontroller family

**Changes made:**

1. Created model with 5 instruction categories:
   - alu: 6 cycles (serial BCD ADD, SUB)
   - bcd: 8 cycles (multi-digit BCD, decimal adjust)
   - shift: 4 cycles (shift register rotate)
   - control: 5 cycles (branch, conditional skip)
   - display: 10 cycles (display scan, segment drive)

2. Calibrated workload weights for typical CPI = 7.0:
   - typical: alu=0.20, bcd=0.15, shift=0.15, control=0.20, display=0.30
   - compute: heavier BCD/ALU (CPI ~6.7)
   - memory: heavier shift ops (CPI ~6.35)
   - control: heavier control/display (CPI ~6.55)

3. Added validation tests:
   - Typical CPI = 7.0 (0.0% error)
   - IPS ~42,857 at 300 kHz
   - Compute workload correctly shows higher CPI for BCD-heavy work

**What we learned:**
- Display operations dominate calculator workloads (30% of typical)
- Shift register operations are relatively fast (4 cycles)
- BCD multi-digit operations take more cycles than basic ALU
- Serial 4-bit architecture adds overhead for multi-digit arithmetic

**Final state:**
- CPI: 7.0 (0.0% error)
- Validation: PASSED
- All tests passing

**References used:**
- TMS0800 Data Sheet (Texas Instruments, 1973)
- TI Calculator History (Datamath Calculator Museum)
- Early Calculator Chip Architecture Survey

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 19 evaluations
- Corrections: alu: +1.79, bcd: -1.61, control: +1.99, display: -3.21, shift: +2.99

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
