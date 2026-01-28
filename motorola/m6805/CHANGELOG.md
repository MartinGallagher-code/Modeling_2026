# M6805 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-28 - Calibration fix

**Session goal:** Fix CPI accuracy (was 63.0% error)

**Changes made:**
1. Recalibrated instruction categories for simplified 8-bit MCU with single accumulator
2. Updated cycle counts: alu @3.5, data_transfer @4.5, memory @6.0, control @5.5, stack @7.0, bit_ops @5.5

**Final state:**
- CPI: 5.00 (0.0% error)
- Validation: PASSED
- Tests: 16/16 passing

---

## 2026-01-28 - Initial model creation and validation

**Session goal:** Create validated model with self-testing capability

**Changes made:**
1. Implemented validate() method with comprehensive tests
2. Created initial CHANGELOG.md and HANDOFF.md

**Final state:**
- CPI: 8.15 (63.0% error from 5.0 target)
- Validation: NEEDS TUNING
- Tests: 15/16 passing

---
