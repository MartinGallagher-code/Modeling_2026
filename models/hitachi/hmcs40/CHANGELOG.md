# Hitachi HMCS40 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the Hitachi HMCS40

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with category-based instruction timing
   - alu: 4.0 cycles - 4-bit ALU with carry @4 cycles
   - data_transfer: 4.0 cycles - Register/accumulator moves @4 cycles
   - memory: 5.0 cycles - ROM/RAM indirect access @5 cycles
   - control: 5.5 cycles - Branch/call/return @5-6 cycles
   - io: 5.0 cycles - LCD controller I/O @5 cycles
   - Reasoning: Cycle counts based on 1980-era 4-bit architecture
   - Result: CPI = 4.700 (4.44% error vs target 4.5)

**What we learned:**
- Hitachi HMCS40 is a 1980 4-bit microcontroller/processor
- 4-bit MCU behind the iconic HD44780 LCD controller

**Final state:**
- CPI: 4.700 (4.44% error)
- Validation: PASSED

**References used:**
- Hitachi HMCS40 datasheet (1980)
- HD44780 technical reference

---
