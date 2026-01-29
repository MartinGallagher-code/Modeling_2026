# Intel 80386 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-28 - Cross-validation with 80x86 family

**Session goal:** Add comprehensive instruction timing tests and cross-validation documentation

**Starting state:**
- CPI: 4.335 (3.7% error)
- Validation: PASSED

**Changes made:**

1. Added 26 per-instruction timing tests to validation JSON
   - ALU: ADD, SUB, CMP, AND, OR, XOR, INC, LEA (2 cycles each)
   - Data transfer: MOV variants (2-4 cycles)
   - Multiply/divide: MUL/DIV 32-bit (14-43 cycles)
   - Control: JMP, Jcc, CALL, RET (3-10 cycles)
   - Memory: PUSH, POP (2-4 cycles)

2. Added cross_validation section documenting:
   - Position as first true 32-bit x86 processor
   - Predecessor: 80286 (added 32-bit, paging, virtual 8086 mode)
   - Successor: 80486 (pipeline, on-chip cache and FPU)
   - Variants: 386DX (32-bit bus), 386SX (16-bit bus), 386SL (mobile)

**What we learned:**
- First x86 to run Unix and Windows in protected mode
- Hardware paging enabled true virtual memory
- No on-chip cache - required external cache for performance
- Required external 80387 coprocessor for FPU
- 32-bit MUL only 14 cycles (vs 40 for DIV)

**Final state:**
- CPI: 4.335 (3.7% error vs expected 4.5)
- Validation: PASSED
- Timing tests: 26 instruction tests added

---

## 2026-01-28 - Initial calibration

**Session goal:** Achieve <5% CPI prediction error

**Starting state:**
- CPI: uncalibrated (high error)
- Key issues: Model used wrong function signature or uncalibrated template

**Changes made:**

1. Rewrote model to use correct analyze() method
   - Replaced simulate() with analyze() returning AnalysisResult
   - Calibrated instruction cycle counts for target CPI
   - Result: Achieved <5% error

**What we learned:**
- The Intel 80386 (1985) was the first 32-bit x86 processor
- 1.5um CMOS technology with 275000 transistors, 16 MHz clock
- Full 32-bit architecture with virtual memory and paging
- Instructions take 2-40 cycles, enabled running Unix and Windows

**Final state:**
- CPI: 4.335 (3.7% error vs expected 4.5)
- Validation: PASSED

---
