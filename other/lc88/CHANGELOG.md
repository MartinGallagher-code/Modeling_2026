# Sanyo LC88 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for Sanyo LC88 16-bit MCU

**Starting state:**
- No model existed

**Research findings:**
- LC88 was Sanyo's 16-bit MCU (1985), upgrade from LC87 8-bit family
- ~20,000 transistors, 8 MHz clock
- 16-bit data path with 20-bit address bus (1MB)
- On-chip ROM, RAM, timer, I/O
- Used in audio/video equipment, consumer electronics
- CPI ~4.0 (improved from LC87's ~5.0)

**Changes made:**

1. Created model with 5 instruction categories:
   - alu: ALU operations @3 cycles
   - data_transfer: MOV/LD (16-bit) @3 cycles
   - memory: Indirect/indexed @5 cycles
   - io: Port read/write @5 cycles
   - control: JP/CALL/RET @4 cycles

2. Added 4 workload profiles:
   - typical: Balanced embedded workload
   - compute: Computation-heavy
   - io_heavy: I/O-intensive (audio/video)
   - control: Control-flow intensive

3. Added validation tests:
   - CPI ~4.0 for typical workload
   - All category timing verified

**What we learned:**
- 16-bit data path reduces CPI vs 8-bit LC87
- I/O improved from 6 to 5 cycles with better port interface
- Control flow improved from 5 to 4 cycles with wider fetch

**Final state:**
- CPI: 3.94 (1.5% error from 4.0 target)
- Validation: PASSED
- 8/8 per-instruction timing tests passing

**References used:**
- Sanyo LC88 Series Data Sheet (1985)
- Sanyo Semiconductor Guide (1986)

---
