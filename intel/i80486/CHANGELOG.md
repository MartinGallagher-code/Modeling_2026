# Intel 80486 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-28 - Cross-validation with 80x86 family

**Session goal:** Add comprehensive instruction timing tests and cross-validation documentation

**Starting state:**
- CPI: 2.05 (2.5% error)
- Validation: PASSED

**Changes made:**

1. Added 29 per-instruction timing tests to validation JSON
   - ALU: ADD, SUB, CMP, AND, OR, XOR, INC, LEA (1 cycle each!)
   - Data transfer: MOV variants (1 cycle with cache hit)
   - Multiply/divide: MUL/DIV 32-bit (13-43 cycles)
   - Control: JMP, Jcc, CALL, RET (1-5 cycles)
   - Memory: PUSH, POP (1 cycle)
   - FPU: FADD, FMUL, FDIV (8-73 cycles) - on-chip!

2. Added cross_validation section documenting:
   - Position as first pipelined x86 with on-chip cache and FPU
   - Predecessor: 80386 (added pipeline, cache, integrated FPU)
   - Successor: Pentium (superscalar, separate I/D cache)
   - Variants: 486DX, 486SX, 486DX2, 486DX4

**What we learned:**
- Most ALU instructions execute in 1 cycle (vs 2 for 386)
- First x86 to break 1 MIPS/MHz barrier
- 5-stage pipeline: Prefetch, Decode1, Decode2, Execute, Writeback
- On-chip FPU is 8-10x faster than external 80387
- Introduced clock multiplying (DX2, DX4)

**Final state:**
- CPI: 2.05 (2.5% error vs expected 2.0)
- Validation: PASSED
- Timing tests: 29 instruction tests added

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
- The Intel 80486 (1989) was the first pipelined x86 with on-chip cache and FPU
- 1um CMOS technology with 1.2 million transistors, 25 MHz base clock
- 5-stage pipeline enabled many instructions to complete in 1 cycle
- First x86 to break 1 MIPS/MHz barrier

**Final state:**
- CPI: 2.05 (2.5% error vs expected 2.0)
- Validation: PASSED

---
