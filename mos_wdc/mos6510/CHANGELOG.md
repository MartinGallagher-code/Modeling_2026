# MOS 6510 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-28 - Cross-validation using 6502 timings

**Session goal:** Apply cross-validated 6502 timings to 6510 (identical instruction set)

**Starting state:**
- CPI: 3.485 (0.4% error vs old target 3.5)
- Using pre-cross-validation 6502 cycle counts

**Changes made:**

1. Applied cross-validated 6502 cycle counts:
   - alu: 3.0 → 2.3 cycles (INX/DEX @2, ADC imm @2, ADC zp @3)
   - data_transfer: 3.5 → 2.8 cycles (LDA imm @2, zp @3, abs @4)
   - memory: 4.2 → 4.0 cycles (STA zp @3, abs @4, indexed @4-5)
   - control: 3.0 → 2.6 cycles (branches @2.55 avg, JMP @3)
   - stack: 3.5 unchanged

2. Updated target CPI from 3.5 to 3.0 (matches cross-validated 6502)

3. Added 17 per-instruction timing tests to validation JSON

**What we learned:**
- 6510 timing is 100% identical to 6502
- Cross-validated CPI of 3.0 is accurate for typical C64 programs
- VICE emulator uses same timing tables

**Final state:**
- CPI: 3.065 (2.17% error vs target 3.0)
- Cross-validated: Yes
- Per-instruction tests: 17/17 passing

---

## 2026-01-28 - Implement validate() method

**Session goal:** Add self-validation capability to the model

**Starting state:**
- CPI: 3.49 (0.4% error) - already passing
- validate() method returned empty results

**Changes made:**

1. Implemented validate() method with 15 tests:
   - CPI accuracy check (target 3.5 +/- 5%)
   - Weights sum to 1.0 for all 4 workload profiles
   - Cycle counts in valid range (1-10) for all 5 categories
   - IPC in expected range (0.15-0.6)
   - All workloads produce valid results

**Final state:**
- 15/15 tests passing
- Accuracy: 99.6%
- Model now self-validates

---

## 2026-01-28 - Initial calibration (same as 6502)

**Session goal:** Fix model that had 132.86% CPI error

**Starting state:**
- CPI: 8.15 (132.86% error vs expected 3.5)
- Key issues: Template had wrong cycle counts, not calibrated to 6502 timings

**Changes made:**

Applied same fix as MOS 6502 model - the 6510 has identical instruction timing.

1. Restructured instruction categories to match 6502
   - alu: 3.0 cycles
   - data_transfer: 3.5 cycles
   - memory: 4.2 cycles
   - control: 3.0 cycles
   - stack: 3.5 cycles

2. Updated workload profiles for C64 typical usage

**What we learned:**

- 6510 is a 6502 with added I/O port at $00-$01
- Instruction timing is 100% identical to 6502
- The I/O port is used for C64 memory banking (ROM/RAM selection)

**Final state:**
- CPI: 3.485 (0.4% error)
- Validation: PASSED

**References used:**
- MOS 6510 datasheet
- VICE emulator (C64 validation)
- 6502 model as baseline

---
