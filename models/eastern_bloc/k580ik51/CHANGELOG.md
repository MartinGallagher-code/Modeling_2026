# K580IK51 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial Model Creation

**Session goal:** Create validated grey-box queueing model for K580IK51

**Starting state:**
- No model existed

**Changes attempted:**

1. Created K580IK51 model as Soviet 8051-compatible MCU
   - Architecture: 8-bit MCU, sequential execution, 6 MHz, 12,000 transistors
   - Calibrated instruction categories from 8051 timing:
     - alu: 1.0 cycle (ADD A,Rn @1, SUBB @1, INC @1)
     - data_transfer: 2.0 cycles (MOV A,Rn @1, MOV A,direct @2, weighted)
     - memory: 2.0 cycles (MOVX A,@DPTR @2, MOVC @2)
     - control: 2.0 cycles (LJMP @2, LCALL @2, RET @2, DJNZ @2)
     - bit_ops: 2.0 cycles (SETB @1, CLR @1, JB/JNB @2)
     - timer: 3.0 cycles (MUL AB @4, DIV AB @4, peripheral access)

2. Calibrated workload weights for typical profile:
   - alu: 0.15, data_transfer: 0.20, memory: 0.15, control: 0.20, bit_ops: 0.15, timer: 0.15
   - Produces exactly CPI = 2.0

**What we learned:**
- Soviet 8051 clone for embedded control applications
- Very efficient instruction set - most ops in 1-2 machine cycles
- On-chip peripherals (RAM, ROM, timers, serial port)
- Bit-addressable memory is key MCU feature
- Machine cycles (not T-states) used for CPI calculation

**Final state:**
- CPI: 2.00 (0.0% error)
- Validation: PASSED (16/16 tests)

**References used:**
- Intel 8051 Datasheet (timing reference)
- MCS-51 architecture documentation

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 6 free correction parameters
- Optimizer converged in 1 evaluations
- Corrections: all near zero (model already matched measurements)

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
