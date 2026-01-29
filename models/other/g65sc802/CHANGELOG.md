# GTE G65SC802 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation and validation

**Session goal:** Create validated model for GTE G65SC802 - WDC 65C816 second-source

**Starting state:**
- No existing model

**Changes made:**

1. Created initial model with 65C816 timing calibrated for CPI = 3.5
   - alu: 2 cycles (ADC, SBC, AND, ORA)
   - data_transfer: 3 cycles (LDA, STA, TAX)
   - memory: 4 cycles (indexed indirect)
   - control: 3 cycles (BNE, JMP, JSR)
   - stack: 4 cycles (PHA, PLA, PEA)
   - long_addr: 5 cycles (24-bit addressing modes)

**What we learned:**
- G65SC802 is GTE's second-source of WDC 65C816
- 6502-compatible 40-pin DIP package
- Same die as G65SC816 but different pinout
- CMOS technology enables 4 MHz operation
- Emulation mode CPI around 3.5

**Final state:**
- CPI: 3.40 (target 3.5, within 5%)
- Validation: PASSED

**References used:**
- WDC 65C816 Data Sheet
- GTE G65SC802 Data Sheet
- Western Design Center programming reference

---
