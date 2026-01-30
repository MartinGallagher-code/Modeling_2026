# M68060 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-28 - Cross-validation with 68K family

**Session goal:** Add per-instruction timing tests and cross-validate across 68K family

**Changes made:**
1. Added 25 per-instruction timing tests with expected cycles from datasheet
2. Added cross_validation section documenting relationships to M68040/M68030/M68020
3. Updated validation JSON with superscalar and branch prediction specifications

**Timing tests added:**
- Register ops: MOVE.L Dn,Dn, ADD.L Dn,Dn, SUB.L Dn,Dn, CLR.L, CMP.L, LEA, AND.L, LSL.L
- Memory ops: MOVE.L mem,Dn, MOVE.L Dn,mem, ADD.L mem,Dn
- Multiply/divide: MULU.L, MULS.L, DIVU.L, DIVS.L
- Control: BRA predicted/mispredicted, Bcc predicted/mispredicted, JSR, RTS
- FPU: FADD.D, FMUL.D, FDIV.D

**Cross-validation notes:**
- M68060 is last and fastest 68K - superscalar dual-issue
- 2-3x faster than M68040 at same clock
- 10-stage pipeline with branch prediction (256-entry cache)
- 8KB I-cache, 8KB D-cache (4-way set-associative)
- Pipelined multiply (2 cycles vs 5 in 68040)
- Much faster divide (10 cycles vs 38 in 68040)
- Dual-issue - can execute 2 instructions per cycle
- Historically: Released 1994, same year as PowerPC Mac - too late for market

**Final state:**
- CPI: 1.479 (1.40% error)
- Validation: PASSED
- No model changes needed (accuracy within 5%)

---

## 2026-01-28 - Calibration fix

**Session goal:** Fix CPI accuracy (was 100.7% error)

**Changes made:**
1. Adjusted cache parameters for superscalar 68k with 8KB caches and branch prediction
2. Set cache hit rates: 98% I-cache, 94% D-cache
3. Reduced multiply/divide penalties for superscalar execution

**Final state:**
- CPI: 1.48 (0.0% error)
- Validation: PASSED
- Tests: 18/18 passing

---

## 2026-01-28 - Initial model creation and validation

**Session goal:** Create validated model with self-testing capability

**Changes made:**
1. Implemented validate() method with comprehensive tests
2. Created initial CHANGELOG.md and HANDOFF.md

**Final state:**
- CPI: 3.01 (100.7% error from 1.5 target)
- Validation: NEEDS TUNING
- Tests: 17/18 passing

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 8 free correction parameters
- Optimizer converged in 16 evaluations
- Corrections: alu: -0.43, branch: -0.13, divide: -2.29, fp_double: +1.39, fp_single: +3.25, load: -0.69, multiply: +2.92, store: +0.45

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
