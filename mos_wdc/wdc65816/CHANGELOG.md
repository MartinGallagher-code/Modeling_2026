# WDC 65816 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-28 - Initial calibration for 16-bit operations

**Session goal:** Fix model that had 98.77% CPI error

**Starting state:**
- CPI: 7.55 (98.77% error vs expected 3.8)
- Key issues: Template was completely wrong (modeled as "Prefetch Queue" architecture)

**Changes made:**

1. Rewrote model from scratch for 65816 architecture
   - Removed prefetch queue modeling (65816 is sequential like 6502)
   - Added proper 16-bit cycle penalties

2. Calibrated cycle counts for 8/16-bit mixed operation
   - alu: 3.2 cycles (+1 in 16-bit mode averaged in)
   - data_transfer: 3.8 cycles (mix of 8/16-bit modes)
   - memory: 4.5 cycles (including long 24-bit addressing)
   - control: 3.5 cycles (branches + JML, JSL)
   - stack: 4.0 cycles (16-bit push/pull are longer)

3. Key 65816 differences from 65C02:
   - 16-bit operations add +1 cycle for extra byte
   - Long addressing (24-bit) adds +1 cycle
   - JSL (jump subroutine long) = 8 cycles
   - RTL (return long) = 6 cycles
   - 16-bit accumulator/index modes

**What we learned:**

- 65816 is slightly slower than 6502/65C02 due to 16-bit overhead
- Expected CPI of 3.8 reflects mixed 8/16-bit operation
- SNES games typically ran in 16-bit mode for most operations
- The 24-bit address space was key for SNES's 128KB+ games

**Final state:**
- CPI: 3.820 (0.5% error)
- Validation: PASSED

**References used:**
- WDC 65816 datasheet
- SNES technical documentation
- Comparison with 65C02 baseline

---
