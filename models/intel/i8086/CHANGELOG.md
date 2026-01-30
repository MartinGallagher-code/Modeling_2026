# Intel 8086 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

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
- The Intel 8086 (1978) was the first x86 processor, foundation of the x86 architecture
- 3um NMOS technology with 29000 transistors, 5 MHz clock
- 16-bit architecture with segment registers for 20-bit addressing (1MB)
- Instructions take 2-200+ cycles, with MUL/DIV being very expensive

**Final state:**
- CPI: 4.525 (0.6% error vs expected 4.5)
- Validation: PASSED

---

## 2026-01-28 - Cross-validation with Intel 8088

**Session goal:** Cross-validate 8086 and 8088 models against Intel datasheet timings

**Starting state:**
- CPI: 4.525 (0.56% error vs expected 4.5)
- Validation: PASSED

**Verification performed:**

1. Verified model instruction categories against Intel datasheet timings:
   - MOV reg,reg: 2 cycles (model uses 2.5 avg for data_transfer category)
   - MOV reg,imm: 4 cycles
   - MOV reg,mem: 8+EA cycles (model uses 7.0 for memory category)
   - ADD reg,reg: 3 cycles (model uses 2.5 for alu category)
   - JMP near: 15 cycles (model uses 10.0 for control category)
   - Category-based averaging is appropriate for grey-box modeling

2. Added comprehensive instruction timing tests (28 tests):
   - Data transfer: MOV reg,reg, MOV reg,imm, LEA, XCHG
   - Memory: MOV reg,mem, MOV mem,reg
   - ALU: ADD, SUB, CMP, AND, OR, XOR, INC, SHL
   - Control: JMP, Jcc taken/not taken, CALL, RET, LOOP, NOP
   - Stack: PUSH, POP
   - Mul/div: MUL word (70-118), DIV word (80-162)
   - String: MOVSB, REP MOVSB

3. Added cross_validation section documenting 8086/8088 relationship:
   - Same internal architecture (16-bit)
   - 8086: 16-bit external bus, 6-byte prefetch queue
   - 8088: 8-bit external bus, 4-byte prefetch queue
   - Performance ratio: 8088 is 86.5% of 8086 speed
   - Memory ops add 4 cycles on 8088 for 16-bit data

**What we learned:**
- The 8086 model uses effective cycle counts that average prefetch queue overlap
- Raw instruction timings from datasheet are 2-200+ cycles
- Effective CPI of 4.5 accounts for BIU/EU parallelism
- Model categories represent weighted averages, not individual instruction timings
- Cross-validation with 8088 confirms the 8-bit bus penalty model is consistent

**Final state:**
- CPI: 4.525 (0.56% error)
- Validation: PASSED
- 28 instruction timing tests documented
- Cross-validation with 8088 complete

**References used:**
- Intel 8086 Datasheet (chipdb.org)
- Intel 8086/8088 User's Manual
- WikiChip 8086 article

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 4 free correction parameters
- Optimizer converged in 2 evaluations
- Corrections: alu: -1.51, control: -2.34, data_transfer: +2.79, memory: -0.87

**Final state:**
- CPI error: 0.48%
- Validation: PASSED

---
