# M68008 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-28 - Cross-validation with 68K family

**Session goal:** Add per-instruction timing tests and cross-validate across 68K family

**Changes made:**
1. Added 25 per-instruction timing tests with expected cycles from datasheet
2. Added cross_validation section documenting relationships to M68000/M68010/M68020
3. Updated validation JSON with detailed specifications and source verification

**Timing tests added:**
- Register ops: MOVE.W/L Dn,Dn, ADD.W/L Dn,Dn, SUB.W Dn,Dn, CLR.L, CMP.W, TST.W, LEA
- Memory ops: MOVE.W/L mem,Dn, MOVE.W/L Dn,mem, ADD.W mem,Dn
- Multiply/divide: MULU.W, MULS.W, DIVU.W, DIVS.W
- Control: NOP, JMP, JSR, RTS, Bcc taken/not_taken, DBcc

**Cross-validation notes:**
- M68008 is 8-bit bus variant of 68000 - same internal timing
- 50-60% slower than M68000 due to 8-bit bus
- Word accesses take 2x cycles, long accesses take 4x cycles

**Final state:**
- CPI: 7.205 (2.93% error)
- Validation: PASSED
- No model changes needed (accuracy within 5%)

---

## 2026-01-28 - Initial model creation and validation

**Session goal:** Create validated model with self-testing capability

**Changes made:**
1. Implemented validate() method with comprehensive tests
2. Created initial CHANGELOG.md and HANDOFF.md

**Final state:**
- CPI: 7.20 (2.9% error)
- Validation: PASSED
- Tests: 16/16 passing

---
