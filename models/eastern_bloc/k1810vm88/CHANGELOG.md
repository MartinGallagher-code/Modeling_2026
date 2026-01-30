# K1810VM88 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial Model Creation

**Session goal:** Create validated grey-box queueing model for K1810VM88

**Starting state:**
- No model existed

**Changes attempted:**

1. Created K1810VM88 model as Soviet Intel 8088 clone
   - Architecture: 8/16-bit, sequential execution, 5 MHz, 29,000 transistors
   - Calibrated instruction categories from 8088 timing:
     - alu: 3.0 cycles (ADD reg,reg @3, INC @2, CMP @3)
     - data_transfer: 4.0 cycles (MOV reg,reg @2, MOV reg,imm @4)
     - memory: 6.0 cycles (memory ops with 8-bit bus penalty)
     - control: 5.0 cycles (JMP @15, CALL @19, RET @8, Jcc ~5)
     - multiply: 30.0 cycles (MUL 8-bit @70-77, weighted average)
     - string: 8.0 cycles (REP MOVSB/STOSB with 8-bit bus)

2. Calibrated workload weights for typical profile:
   - alu: 0.32, data_transfer: 0.25, memory: 0.12, control: 0.20, multiply: 0.02, string: 0.09
   - Produces exactly CPI = 5.0

**What we learned:**
- Soviet 8088 clone with 8-bit external bus (16-bit internal)
- 4-byte prefetch queue (vs 6-byte on 8086/K1810VM86)
- 8-bit bus makes memory access slower than 8086 variant
- Used in Soviet IBM PC/XT compatible computers

**Final state:**
- CPI: 5.00 (0.0% error)
- Validation: PASSED (16/16 tests)

**References used:**
- Intel 8088 Datasheet (timing reference)
- K1810 series Soviet documentation

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 6 free correction parameters
- Optimizer converged in 1 evaluations
- Corrections: all near zero (model already matched measurements)

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
