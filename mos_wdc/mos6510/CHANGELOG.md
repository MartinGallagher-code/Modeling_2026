# MOS 6510 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

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
