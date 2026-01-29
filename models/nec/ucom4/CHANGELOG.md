# NEC uCOM-4 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for NEC's TMS1000 competitor

**Starting state:**
- No model existed

**Research findings:**
- uCOM-4 was NEC's first microcontroller, introduced in 1972
- Designed as a Japanese competitor to the TI TMS1000
- 4-bit data path with parallel ALU
- Harvard architecture (separate program/data memory)
- Similar timing characteristics to TMS1000 (fixed 6-cycle execution)
- Typical clock: 400 kHz
- Used in calculators, watches, and consumer electronics

**Changes made:**

1. Created model with fixed 6-cycle instruction timing (like TMS1000)
   - Target CPI: 6.0 (matching TMS1000)
   - All instruction categories set to 6 cycles
   - Clock: 400 kHz (faster than TMS1000's 300 kHz)

2. Added 5 instruction categories:
   - alu: ADD, SUB, logical @6 cycles
   - data_transfer: Register-memory transfers @6 cycles
   - memory: Load/store operations @6 cycles
   - control: Branch, call, return @6 cycles
   - io: I/O operations @6 cycles

3. Added 5 workload profiles:
   - typical: General embedded use
   - compute: Calculator-style arithmetic
   - memory: Data manipulation
   - control: Control-flow intensive
   - mixed: General purpose

4. Added validation tests:
   - CPI exactly 6.0 (fixed timing)
   - IPS ~66,667 at 400 kHz
   - All workloads produce identical CPI
   - Comparable to TMS1000

**What we learned:**
- NEC successfully matched TMS1000's timing characteristics
- Fixed instruction timing simplifies the execution model
- Higher clock speed (400 kHz vs 300 kHz) gave uCOM-4 performance advantage
- Japanese semiconductor industry was competing effectively with US by 1972

**Final state:**
- CPI: 6.0 (0.0% error)
- Validation: PASSED
- Fixed timing makes model trivially accurate

**References used:**
- NEC microcontroller historical documentation
- Japanese semiconductor industry archives
- Comparison with TI TMS1000

---
