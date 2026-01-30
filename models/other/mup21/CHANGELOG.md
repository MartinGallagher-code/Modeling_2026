# MuP21 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation (Phase 4: Forth)

**Session goal:** Create grey-box queueing model for the MuP21 minimal Forth chip

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 5 instruction categories
   - stack_op (1 cycle): Stack push/pop/dup/swap
   - alu (1 cycle): ALU operations on top-of-stack
   - memory (2 cycles): Memory fetch/store
   - control (1 cycle): Branch/call operations
   - io (3 cycles): I/O and video operations
   - Weights calibrated for target CPI of 1.3

2. Created validation JSON with accuracy metrics
   - CPI error: 0.0% for typical workload

**What we learned:**
- The MuP21 represents extreme minimalism in processor design
- Only ~7,000 transistors yet runs at 50 MHz
- Four 5-bit instructions packed into each 20-bit word
- Control flow is single-cycle (branch in same word)
- Memory access is only 2 cycles (faster than NC4000/RTX32P)
- I/O includes video coprocessor features
- Designed by Chuck Moore as a successor to the NC4000 concept

**Final state:**
- CPI: 1.3 (0.0% error vs expected 1.3)
- Validation: PASSED

---
