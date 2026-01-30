# Zilog Z280 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the Zilog Z280

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with category-based instruction timing
   - alu: 3.5 cycles - Z80-compat ALU with cache @3-4 cycles
   - data_transfer: 3.5 cycles - Register transfers @3-4 cycles
   - memory: 5.0 cycles - Memory with cache @4-7 cycles
   - control: 5.0 cycles - Branch/call @4-8 cycles
   - stack: 8.0 cycles - Stack ops @7-10 cycles
   - Reasoning: Cycle counts based on 1985-era 8-bit architecture
   - Result: CPI = 5.000 (11.11% error vs target 4.5)

**What we learned:**
- Zilog Z280 is a 1985 8-bit microcontroller/processor
- Enhanced Z80 with MMU, 256-byte cache, and on-chip peripherals

**Final state:**
- CPI: 5.000 (11.11% error)
- Validation: MARGINAL

**References used:**
- Zilog Z280 MPU datasheet (1985)
- Z280 Technical Manual

---
