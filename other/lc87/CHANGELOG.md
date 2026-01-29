# Sanyo LC87 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for Sanyo LC87 8-bit MCU

**Starting state:**
- No model existed

**Research findings:**
- LC87 was Sanyo's 8-bit MCU family (1983)
- ~8,000 transistors, 4 MHz clock
- On-chip ROM, RAM, I/O ports, timer
- Used in audio equipment, home appliances, consumer electronics
- Simple sequential execution, CPI ~5.0

**Changes made:**

1. Created model with 5 instruction categories:
   - alu: ALU operations @3 cycles
   - data_transfer: MOV/LD @4 cycles
   - memory: Indirect/indexed @6 cycles
   - io: Port read/write @6 cycles
   - control: JP/CALL/RET @5 cycles

2. Added 4 workload profiles:
   - typical: Balanced embedded workload
   - compute: Computation-heavy
   - io_heavy: I/O-intensive (audio control)
   - control: Control-flow intensive

3. Added validation tests:
   - CPI ~5.0 for typical workload
   - All category timing verified

**What we learned:**
- Simple 8-bit MCU with straightforward timing
- Memory and I/O operations are equally expensive at 6 cycles
- ALU operations are fastest at 3 cycles

**Final state:**
- CPI: 4.92 (1.6% error from 5.0 target)
- Validation: PASSED
- 8/8 per-instruction timing tests passing

**References used:**
- Sanyo LC87 Series Data Sheet (1983)
- Sanyo Semiconductor Guide (1984)

---
