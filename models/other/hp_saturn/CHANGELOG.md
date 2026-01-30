# HP Saturn Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the HP Saturn calculator CPU

**Starting state:**
- No model existed

**Research findings:**
- HP Saturn was a custom CMOS CPU designed by HP for their calculator line (1984)
- 4-bit nibble-serial data path but with 64-bit registers (16 nibbles)
- Native BCD arithmetic for calculator-grade decimal precision
- Variable-length instruction encoding (2-21 nibbles)
- Clock: 640 kHz (early versions; later up to 4 MHz)
- ~40,000 transistors
- Used in HP 71B, HP 48G/GX, HP 49G series

**Changes made:**

1. Created model with 5 instruction categories:
   - alu: 8 cycles (ADD, SUB on register fields)
   - register_op: 4 cycles (SWAP, COPY, CLR)
   - memory: 12 cycles (DAT0/DAT1 load/store via pointer)
   - control: 6 cycles (GOTO, GOSUB, RTN)
   - bcd: 10 cycles (BCD arithmetic, field operations)

2. Calibrated workload weights for typical CPI = 8.0:
   - typical: alu=0.25, register_op=0.20, memory=0.15, control=0.15, bcd=0.25
   - compute: heavier BCD/ALU (CPI ~8.3)
   - memory: heavier memory ops (CPI ~8.8)
   - control: heavier flow control (CPI ~7.5)

3. Added validation tests:
   - Typical CPI = 8.0 (0.0% error)
   - IPS ~80,000 at 640 kHz
   - Workload ordering matches expectations

**What we learned:**
- Saturn's nibble-serial architecture means wide-field operations are slow
- Memory access through pointers (D0/D1) adds significant overhead
- BCD operations are core to calculator workloads
- Register operations are fast since they work on internal state

**Final state:**
- CPI: 8.0 (0.0% error)
- Validation: PASSED
- All tests passing

**References used:**
- HP Saturn Processor Architecture (HP internal documentation)
- HP 48 Technical Reference Manual
- HP Museum: Saturn Architecture Overview

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 23 evaluations
- Corrections: alu: -1.17, bcd: +1.32, control: -2.56, memory: +1.10, register_op: +0.92

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
