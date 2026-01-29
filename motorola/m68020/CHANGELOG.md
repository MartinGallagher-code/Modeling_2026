# M68020 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-28 - Cross-validation with 68K family

**Session goal:** Add per-instruction timing tests and cross-validate across 68K family

**Changes made:**
1. Added 25 per-instruction timing tests with expected cycles from datasheet
2. Added cross_validation section documenting relationships to M68010/M68030/M68040
3. Updated validation JSON with detailed specifications and source verification

**Timing tests added:**
- Register ops: MOVE.L Dn,Dn, ADD.L Dn,Dn, SUB.L Dn,Dn, CLR.L, CMP.L, LEA
- Logical: AND.L, OR.L, EOR.L, LSL.L
- Memory ops: MOVE.L mem,Dn, MOVE.L Dn,mem, ADD.L mem,Dn
- Multiply/divide: MULU.L, MULS.L, DIVU.L, DIVS.L
- Control: NOP, BRA.W, Bcc taken/not_taken, JSR, RTS, BFxxx, CHK2

**Cross-validation notes:**
- M68020 is first full 32-bit 68K with instruction cache
- 3-4x faster than M68010
- 256-byte instruction cache eliminates fetch overhead
- First with bit field instructions (BFxxx)

**Final state:**
- CPI: 3.525 (0.71% error)
- Validation: PASSED
- No model changes needed (accuracy within 5%)

---

## 2026-01-28 - Initial model creation and validation

**Session goal:** Create validated model with self-testing capability

**Changes made:**
1. Implemented validate() method with comprehensive tests
2. Created initial CHANGELOG.md and HANDOFF.md

**Final state:**
- CPI: 3.53 (0.7% error)
- Validation: PASSED
- Tests: 16/16 passing

---
