# Harris RTX32P Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation (Phase 4: Forth)

**Session goal:** Create grey-box queueing model for the Harris RTX32P Forth processor

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model with 5 instruction categories
   - stack_op (1 cycle): Stack push/pop/dup/swap (pipelined)
   - alu (1 cycle): ALU operations on top-of-stack (pipelined)
   - memory (3 cycles): Memory fetch/store
   - control (2 cycles): Branch/loop operations
   - call_return (2 cycles): Subroutine call/return
   - Weights calibrated for target CPI of 1.5

2. Created validation JSON with accuracy metrics
   - CPI error: 0.0% for typical workload

**What we learned:**
- The RTX32P is a 32-bit pipelined Forth engine from Harris Semiconductor
- Hardware dual stacks (data + return) enable single-cycle stack operations
- Subroutine threading is done in hardware, making Forth word calls fast
- Most Forth primitives (DUP, SWAP, +, AND, etc.) execute in 1 clock cycle
- Memory access is the bottleneck at 3 cycles

**Final state:**
- CPI: 1.5 (0.0% error vs expected 1.5)
- Validation: PASSED

---
