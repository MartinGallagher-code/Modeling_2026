# WDC 65C02 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-28 - Implement validate() method

**Session goal:** Add self-validation capability to the model

**Starting state:**
- CPI: 3.20 (0.0% error) - already passing
- validate() method returned empty results

**Changes made:**

1. Implemented validate() method with 16 tests:
   - CPI accuracy check (target 3.2 +/- 5%)
   - Weights sum to 1.0 for all 4 workload profiles
   - Cycle counts in valid range (1-10) for all 5 categories
   - IPC in expected range (0.15-0.6)
   - 65C02 faster than 6502 check (CPI < 3.5)
   - All workloads produce valid results

**Final state:**
- 16/16 tests passing
- Accuracy: 100.0%
- Model now self-validates

---

## 2026-01-28 - Initial calibration for CMOS optimizations

**Session goal:** Fix model that had 154.69% CPI error

**Starting state:**
- CPI: 8.15 (154.69% error vs expected 3.2)
- Key issues: Template had wrong cycle counts, didn't reflect CMOS optimizations

**Changes made:**

1. Calibrated for 65C02-specific optimizations
   - alu: 2.8 cycles (slightly faster than 6502's 3.0)
   - data_transfer: 3.2 cycles (optimized indexed modes)
   - memory: 3.8 cycles (faster indexed operations)
   - control: 2.8 cycles (includes BRA instruction)
   - stack: 3.2 cycles (includes PHX/PHY/PLX/PLY)

2. Key 65C02 improvements over 6502:
   - Indexed addressing modes no longer have dummy read cycles
   - Read-modify-write on abs,X is 1 cycle faster
   - New BRA (branch always) = 3 cycles vs conditional+JMP combo
   - New PHX/PHY/PLX/PLY for faster register save/restore

**What we learned:**

- 65C02 is genuinely faster than 6502 (CPI 3.2 vs 3.5)
- CMOS allowed bug fixes that also improved timing
- BRA instruction significantly helps control flow
- The 65C02 can run at much higher clock speeds (up to 14 MHz)

**Final state:**
- CPI: 3.200 (0.0% error)
- Validation: PASSED

**References used:**
- WDC 65C02 datasheet
- Comparison with 6502 timings
- Apple IIc/IIe Enhanced documentation

---
