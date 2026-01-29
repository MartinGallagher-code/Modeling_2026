# M68010 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-28 - Cross-validation with 68K family

**Session goal:** Add per-instruction timing tests and cross-validate across 68K family

**Changes made:**
1. Added 25 per-instruction timing tests with expected cycles from datasheet
2. Added cross_validation section documenting relationships to M68000/M68008/M68020
3. Updated validation JSON with detailed specifications and source verification

**Timing tests added:**
- Register ops: MOVE.W/L Dn,Dn, ADD.W/L Dn,Dn, SUB.W Dn,Dn, CLR.L, CMP.W, LEA
- Memory ops: MOVE.W/L mem,Dn, MOVE.W/L Dn,mem, ADD.W mem,Dn
- Multiply/divide: MULU.W, MULS.W, DIVU.W, DIVS.W
- Control: NOP, JMP, JSR, RTS, Bcc taken/not_taken, DBcc_loop_mode, MOVEC, MOVEP.L

**Cross-validation notes:**
- M68010 is enhanced M68000 with VM support and loop mode
- 5-10% faster than M68000 due to loop mode optimization
- DBcc loops can save 2-3 cycles per iteration
- Same 16-bit bus as M68000

**Final state:**
- CPI: 5.775 (3.75% error)
- Validation: PASSED
- No model changes needed (accuracy within 5%)

---

## 2026-01-28 - Initial model creation and validation

**Session goal:** Create validated model with self-testing capability

**Changes made:**
1. Implemented validate() method with comprehensive tests
2. Created initial CHANGELOG.md and HANDOFF.md

**Final state:**
- CPI: 5.77 (3.8% error)
- Validation: PASSED
- Tests: 16/16 passing

---
