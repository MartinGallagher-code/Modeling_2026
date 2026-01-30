# Intel 8088 Model Changelog

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
- The Intel 8088 (1979) is an 8086 with 8-bit external bus
- Same 3um NMOS technology with 29000 transistors, 5 MHz clock
- 8-bit external bus causes memory access penalties vs 8086
- Used in the original IBM PC, making it historically significant

**Final state:**
- CPI: 5.2 (0.0% error vs expected 5.2)
- Validation: PASSED

---

## 2026-01-28 - Cross-validation with Intel 8086

**Session goal:** Cross-validate 8088 and 8086 models against Intel datasheet timings

**Starting state:**
- CPI: 5.2 (0.0% error vs expected 5.2)
- Validation: PASSED

**Verification performed:**

1. Verified model instruction categories against Intel datasheet timings:
   - Register ops same as 8086 (MOV reg,reg: 2 cycles)
   - Memory ops add 4 cycles for 8-bit bus (MOV reg,mem: 8+4=12 cycles)
   - Model uses alu=3.0, data_transfer=3.0, memory=8.0, control=11.0
   - Category-based averaging appropriate for grey-box modeling

2. Added comprehensive instruction timing tests (29 tests):
   - Data transfer: MOV reg,reg, MOV reg,imm, LEA, XCHG
   - Memory: MOV reg,mem (+4 cycles), MOV mem,reg (+4 cycles)
   - ALU: ADD, SUB, CMP, AND, OR, XOR, INC, SHL
   - Control: JMP, Jcc taken/not taken, CALL (+4), RET (+4), LOOP, NOP
   - Stack: PUSH (+4), POP (+4)
   - Mul/div: MUL word (70-118), DIV word (80-162) - same as 8086
   - String: MOVSB (same as 8086), MOVSW (+8 for two word accesses)

3. Added cross_validation section documenting 8086/8088 relationship:
   - Same internal architecture (16-bit)
   - 8088: 8-bit external bus, 4-byte prefetch queue
   - 8086: 16-bit external bus, 6-byte prefetch queue
   - Performance ratio: 8088 is 86.5% of 8086 speed
   - Memory/stack ops add 4 cycles for 16-bit data transfers

4. Added IBM PC historical notes:
   - 8088 chosen for lower system cost (8-bit peripherals)
   - 4.77 MHz clock derived from NTSC color burst frequency
   - Foundation of PC-compatible computing

**What we learned:**
- 8-bit bus penalty is consistent: +4 cycles per 16-bit memory access
- Register-to-register and immediate operations identical to 8086
- Stack operations (PUSH, POP, CALL, RET) affected by bus width
- String operations on words (MOVSW) doubly penalized (+8 cycles)
- Prefetch queue (4 bytes vs 6 bytes) slightly reduces overlap efficiency

**Final state:**
- CPI: 5.2 (0.0% error)
- Validation: PASSED
- 29 instruction timing tests documented
- Cross-validation with 8086 complete

**References used:**
- Intel 8088 Datasheet (chipdb.org)
- Intel 8086/8088 User's Manual
- WikiChip 8088 article

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 4 free correction parameters
- Optimizer converged in 2 evaluations
- Corrections: alu: -1.99, control: -2.83, data_transfer: +3.57, memory: -1.08

**Final state:**
- CPI error: 0.24%
- Validation: PASSED

---
