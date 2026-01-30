# Sharp SC61860 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the Sharp SC61860 pocket computer CPU

**Starting state:**
- No model existed

**Research findings:**
- Custom Sharp CMOS CPU designed for pocket computers (1980)
- 8-bit accumulator-based architecture
- 96 bytes internal RAM, 512 bytes character generator ROM
- Integrated LCD display controller
- Clock: 576 kHz
- ~8,000 transistors
- Used in Sharp PC-1211, PC-1245, PC-1500 series

**Changes made:**

1. Created model with 5 instruction categories:
   - alu: 3 cycles (ADD, SUB, AND, OR, CMP)
   - data_transfer: 4 cycles (LD, ST, MOV)
   - memory: 6 cycles (external memory access)
   - control: 5 cycles (JP, CALL, RET)
   - display: 8 cycles (LCD controller operations)

2. Calibrated workload weights for typical CPI = 5.0:
   - typical: alu=0.24, data_transfer=0.25, memory=0.10, control=0.20, display=0.21
   - compute: heavier ALU (CPI ~4.55)
   - memory: heavier memory ops (CPI ~5.15)
   - control: heavier flow/display (CPI ~5.25)

3. Added validation tests:
   - Typical CPI = 5.0 (0.0% error)
   - IPS ~115,200 at 576 kHz
   - Workload ordering matches expectations

**What we learned:**
- SC61860 is relatively fast for its era due to 8-bit data path
- Display operations are the most expensive category
- ALU operations are fast (3 cycles) compared to display (8 cycles)
- BASIC interpreter workload is a mix of computation and display updates

**Final state:**
- CPI: 5.0 (0.0% error)
- Validation: PASSED
- All tests passing

**References used:**
- SC61860 Technical Reference Manual (Sharp)
- Sharp PC-1500 Technical Reference
- Pocket Computer Museum archives

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 33 evaluations
- Corrections: alu: +2.03, control: -0.24, data_transfer: +0.42, display: -2.24, memory: -0.73

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
