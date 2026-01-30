# NEC uPD7801 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the NEC uPD7801

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with category-based instruction timing
   - alu: 4.5 cycles - ALU register ops @4-5 cycles
   - data_transfer: 4.0 cycles - Register transfers @3-5 cycles
   - memory: 7.0 cycles - Memory access @6-8 cycles
   - control: 8.0 cycles - Branch/call @7-12 cycles
   - stack: 9.0 cycles - Stack operations @8-10 cycles
   - Reasoning: Cycle counts based on 1980-era 8-bit architecture
   - Result: CPI = 6.500 (8.33% error vs target 6.0)

**What we learned:**
- NEC uPD7801 is a 1980 8-bit microcontroller/processor
- NEC proprietary 8-bit MCU with large Japanese market share

**Final state:**
- CPI: 6.500 (8.33% error)
- Validation: MARGINAL

**References used:**
- NEC uPD7801 datasheet (1980)
- NEC 78K family reference

---
