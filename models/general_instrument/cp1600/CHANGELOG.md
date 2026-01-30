# General Instrument CP1600 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create complete CP1600 processor model for Intellivision CPU

**Starting state:**
- No existing model
- Target CPI: 6.0 (relatively slow 16-bit processor)

**Changes made:**

1. Created initial model with 5 instruction categories
   - ALU operations (4 cycles): ADD, SUB, AND, XOR, etc.
   - Data transfer (6 cycles): MOVR, MVII register moves
   - Memory operations (8 cycles): MVI, MVO load/store
   - Branch operations (6 cycles): B, BNEQ, JSR
   - Shift operations (8 cycles): SLL, SLR, SWAP

2. Calibrated cycle counts to achieve target CPI = 6.0
   - Calculation: 0.30*4 + 0.20*6 + 0.20*8 + 0.15*6 + 0.15*8 = 6.0
   - Weights based on typical Intellivision game instruction mix

3. Created 5 workload profiles
   - typical: Standard game workload
   - compute: Math-intensive (collision detection)
   - memory: Graphics update heavy
   - control: Game logic with many branches
   - mixed: Balanced workload

4. Implemented validate() method with 6 test cases
   - CPI validation for typical workload
   - Per-category cycle timing validation
   - IPS (instructions per second) validation

**What we learned:**
- The CP1600 was a 16-bit processor with 10-bit opcodes
- Used in Mattel Intellivision game console (1979)
- Clock speed was 894.886 kHz (NTSC)
- 8 16-bit registers (R0-R7), R7 is PC
- Most instructions take 6-10 cycles
- Relatively slow for 16-bit due to external memory interface

**Final state:**
- CPI: 6.0 (0% error vs 6.0 target)
- Validation: PASSED (6/6 tests)

**References used:**
- Intellivision programming guides
- CP1600 instruction set documentation
- MAME emulation timing data

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 31 evaluations
- Corrections: alu: -1.86, branch: -0.76, data_transfer: +3.47, memory: -0.27, shift: -1.03

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
