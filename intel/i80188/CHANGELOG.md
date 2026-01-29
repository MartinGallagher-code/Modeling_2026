# Intel 80188 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-28 - Cross-validation with 80x86 family

**Session goal:** Add comprehensive instruction timing tests and cross-validation documentation

**Starting state:**
- CPI: 4.155 (1.1% error)
- Validation: PASSED

**Changes made:**

1. Added 25 per-instruction timing tests to validation JSON
   - ALU: ADD, SUB, CMP, AND, OR, XOR, INC (2 cycles each)
   - Data transfer: MOV variants (2-7 cycles, slower for memory due to 8-bit bus)
   - Multiply/divide: MUL/DIV 16-bit (36-44 cycles)
   - Control: JMP, Jcc, CALL, RET (4-13 cycles)
   - Memory: PUSH, POP (6 cycles - extra cycle for 8-bit bus)

2. Added cross_validation section documenting:
   - Position as 8-bit bus 80186 for cost-sensitive embedded
   - Predecessor: 8088 (faster microcode, integrated peripherals)
   - Sibling: 80186 (16-bit bus, ~5% faster)
   - Successor: 80286 (protected mode, PC market)

**What we learned:**
- Word operations require two bus cycles (8-bit bus)
- Register operations identical to 80186 in timing
- Memory operations ~1 cycle slower than 80186 for word access
- Prefetch queue starves more easily than 80186

**Final state:**
- CPI: 4.155 (1.1% error vs expected 4.2)
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
- The Intel 80188 (1982) was the 80186 with 8-bit external bus
- Same NMOS technology with 55000 transistors, 8 MHz clock
- 8-bit external bus causes memory access penalties vs 80186
- Used in cost-sensitive embedded applications

**Final state:**
- CPI: 4.155 (1.1% error vs expected 4.2)
- Validation: PASSED

---
