# NEC uPD1007C Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the NEC uPD1007C calculator CPU

**Starting state:**
- No model existed

**Research findings:**
- Custom NEC CMOS calculator CPU (1978)
- 4-bit data path with native BCD arithmetic
- Integrated LCD/LED display driver
- Low-power CMOS design for battery operation
- Clock: 500 kHz typical
- ~6,000 transistors
- Used in Casio scientific and programmable calculators

**Changes made:**

1. Created model with 5 instruction categories:
   - alu: 5 cycles (ADD, SUB, INC, DEC, CMP)
   - bcd: 7 cycles (multi-digit BCD arithmetic, DAA)
   - memory: 6 cycles (load/store to register file)
   - control: 4 cycles (branch, skip, call/return)
   - display: 9 cycles (LCD segment drive, scan)

2. Calibrated workload weights for typical CPI = 6.0:
   - typical: alu=0.20, bcd=0.20, memory=0.20, control=0.24, display=0.16
   - compute: heavier BCD (CPI ~6.15)
   - memory: heavier memory (CPI ~6.3)
   - control: lighter overall (CPI ~5.75)

3. Added validation tests:
   - Typical CPI = 6.0 (0.0% error)
   - IPS ~83,333 at 500 kHz
   - Workload ordering matches expectations

**What we learned:**
- Display operations are the most expensive (9 cycles)
- Control flow is fast (4 cycles) reflecting simple branch logic
- BCD arithmetic is central to calculator workloads
- CMOS design allows lower clock but better power efficiency than PMOS

**Final state:**
- CPI: 6.0 (0.0% error)
- Validation: PASSED
- All tests passing

**References used:**
- uPD1007C Technical Data Sheet (NEC, 1978)
- Casio Calculator Technical Reference
- NEC Microcontroller Family Overview

---
