# Intel 80186 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-28 - Cross-validation with 80x86 family

**Session goal:** Add comprehensive instruction timing tests and cross-validation documentation

**Starting state:**
- CPI: 3.85 (3.8% error)
- Validation: PASSED

**Changes made:**

1. Added 25 per-instruction timing tests to validation JSON
   - ALU: ADD, SUB, CMP, AND, OR, XOR, INC (2 cycles each)
   - Data transfer: MOV reg/imm/mem variants (2-6 cycles)
   - Multiply/divide: MUL/DIV 16-bit (36-44 cycles)
   - Control: JMP, Jcc, CALL, RET (4-12 cycles)
   - Memory: PUSH, POP (5 cycles)

2. Added cross_validation section documenting:
   - Position as enhanced 8086 for embedded market
   - Predecessor: 8086 (faster microcode, integrated peripherals)
   - Successor: 80286 (protected mode, PC market)
   - 80186/80188 sibling relationship

**What we learned:**
- 80186 MUL instruction ~3x faster than 8086 (36 vs 118-133 cycles)
- Same instruction set as 8086 but with optimized microcode
- Integrated peripherals (DMA, timers, interrupt controller) made it ideal for embedded
- 80188 is bus-reduced variant like 8088 vs 8086

**Final state:**
- CPI: 3.85 (3.8% error vs expected 4.0)
- Validation: PASSED
- Timing tests: 25 instruction tests added

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
- The Intel 80186 (1982) integrated 8086 with peripherals on one chip
- 16-bit architecture with NMOS technology, 55000 transistors
- 8 MHz clock with improved instruction timings vs 8086
- Included DMA, timers, and interrupt controller on-chip

**Final state:**
- CPI: 3.85 (3.8% error vs expected 4.0)
- Validation: PASSED

---
