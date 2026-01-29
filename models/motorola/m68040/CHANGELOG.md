# M68040 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-28 - Cross-validation with 68K family

**Session goal:** Add per-instruction timing tests and cross-validate across 68K family

**Changes made:**
1. Added 25 per-instruction timing tests with expected cycles from datasheet
2. Added cross_validation section documenting relationships to M68030/M68060
3. Updated validation JSON with detailed FPU and cache specifications

**Timing tests added:**
- Register ops: MOVE.L Dn,Dn, ADD.L Dn,Dn, SUB.L Dn,Dn, CLR.L, CMP.L, LEA
- Memory ops: MOVE.L mem,Dn, MOVE.L Dn,mem, ADD.L mem,Dn
- Multiply/divide: MULU.L, MULS.L, DIVU.L, DIVS.L
- Control: NOP, BRA taken/not_taken, Bcc taken/not_taken, JSR, RTS
- FPU (68040 new): FADD.S, FMUL.S, FDIV.S, FSQRT.S
- Cache: CINV

**Cross-validation notes:**
- M68040 is first 68K with on-chip FPU
- 2-3x faster than M68030 at same clock
- 6-stage pipeline (vs 3-stage in 68020/030)
- 4KB I-cache, 4KB D-cache (4-way set-associative)
- Pipelined multiply (5 cycles vs 28 in 68030)

**Final state:**
- CPI: 2.035 (1.75% error)
- Validation: PASSED
- No model changes needed (accuracy within 5%)

---

## 2026-01-28 - Initial model creation and validation

**Session goal:** Create validated model with self-testing capability

**Changes made:**
1. Implemented validate() method with comprehensive tests
2. Created initial CHANGELOG.md and HANDOFF.md

**Final state:**
- CPI: 2.04 (1.8% error)
- Validation: PASSED
- Tests: 17/17 passing

---
