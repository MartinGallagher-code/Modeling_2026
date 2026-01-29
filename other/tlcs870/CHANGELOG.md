# Toshiba TLCS-870 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for Toshiba TLCS-870 8-bit MCU

**Starting state:**
- No model existed

**Research findings:**
- TLCS-870 was Toshiba's proprietary 8-bit MCU (1985)
- ~15,000 transistors, 8 MHz clock
- Unique ISA not compatible with Z80 or 6502
- Bit manipulation instructions for embedded I/O control
- On-chip ROM, RAM, timer, UART, I/O
- CPI ~4.5 for typical embedded workloads

**Changes made:**

1. Created model with 6 instruction categories:
   - alu: ALU operations @3 cycles
   - data_transfer: LD/MOV @3 cycles
   - memory: Indirect/indexed @5 cycles
   - io: Port operations @6 cycles
   - control: JP/CALL/RET @5 cycles
   - bit_ops: SET/CLR/TEST @3 cycles

2. Added 4 workload profiles:
   - typical: Balanced embedded workload
   - compute: Computation-heavy
   - io_heavy: I/O and bit manipulation heavy
   - control: Control-flow intensive

3. Added validation tests:
   - CPI ~4.5 for typical workload
   - All category timing verified

**What we learned:**
- Proprietary ISA allows efficient bit manipulation at same cost as ALU ops
- I/O operations are slowest due to port synchronization overhead
- Memory indirect addressing adds 2 cycles vs register operations

**Final state:**
- CPI: 4.44 (1.33% error from 4.5 target)
- Validation: PASSED
- 8/8 per-instruction timing tests passing

**References used:**
- Toshiba TLCS-870 Series Data Sheet (1985)
- Toshiba 8-bit MCU Family Guide

---
