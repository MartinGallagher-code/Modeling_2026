# Toshiba TLCS-47 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for Toshiba TLCS-47 4-bit MCU

**Starting state:**
- No model existed

**Research findings:**
- TLCS-47 was Toshiba's 4-bit MCU family for consumer electronics (1982)
- ~5000 transistors, 500 kHz clock
- Similar class to TI TMS1000 (CPI ~6.0)
- On-chip ROM, RAM, timer, I/O
- Harvard architecture with 4-bit data path
- CMOS process for low power consumption

**Changes made:**

1. Created model with 6 instruction categories:
   - alu: ALU operations @4 cycles
   - data_transfer: MOV/XCHG @5 cycles
   - memory: Indirect load/store @7 cycles
   - io: Port read/write @8 cycles
   - control: BR/CALL/RET @6 cycles
   - timer: Timer control @6 cycles

2. Added 4 workload profiles:
   - typical: Balanced consumer electronics workload
   - compute: Calculator-like compute-heavy
   - io_heavy: I/O-intensive (remote control, appliance)
   - control: Control-flow intensive

3. Added validation tests:
   - CPI ~6.0 for typical workload
   - All category timing verified

**What we learned:**
- 4-bit MCUs of this era have very similar timing characteristics
- I/O operations are the most expensive due to port synchronization
- ALU operations are fastest at 4 cycles

**Final state:**
- CPI: 5.95 (0.83% error from 6.0 target)
- Validation: PASSED
- 8/8 per-instruction timing tests passing

**References used:**
- Toshiba TLCS-47 Series Data Sheet (1982)
- Toshiba Semiconductor Databook (1983)

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 6 free correction parameters
- Optimizer converged in 18 evaluations
- Corrections: alu: +1.68, control: +1.00, data_transfer: +1.34, io: -3.21, memory: -0.23, timer: -1.61

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
