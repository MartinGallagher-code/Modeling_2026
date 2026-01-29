# M68030 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-28 - Cross-validation with 68K family

**Session goal:** Add per-instruction timing tests and cross-validate across 68K family

**Changes made:**
1. Added 25 per-instruction timing tests with expected cycles from datasheet
2. Added cross_validation section documenting relationships to M68020/M68010/M68040
3. Updated validation JSON with detailed cache and MMU specifications

**Timing tests added:**
- Register ops: MOVE.L Dn,Dn, ADD.L Dn,Dn, SUB.L Dn,Dn, CLR.L, CMP.L, LEA
- Logical: AND.L, OR.L
- Memory ops: MOVE.L mem,Dn, MOVE.L Dn,mem, ADD.L mem,Dn
- Multiply/divide: MULU.L, MULS.L, DIVU.L, DIVS.L
- Control: NOP, BRA.W, Bcc taken/not_taken, JSR, RTS
- MMU/cache (68030 new): PFLUSH, PTEST, CINV, CPUSH

**Cross-validation notes:**
- M68030 is M68020 with on-chip MMU and data cache
- 20-30% faster than M68020 due to data cache
- First 68K with on-chip MMU (vs external 68851)
- 256-byte I-cache and D-cache (direct-mapped)

**Final state:**
- CPI: 3.010 (0.33% error)
- Validation: PASSED
- No model changes needed (accuracy within 5%)

---

## 2026-01-28 - Initial model creation and validation

**Session goal:** Create validated model with self-testing capability

**Changes made:**
1. Implemented validate() method with comprehensive tests
2. Created initial CHANGELOG.md and HANDOFF.md

**Final state:**
- CPI: 3.01 (0.3% error)
- Validation: PASSED
- Tests: 18/18 passing

---
