# GTE G65SC816 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation and validation

**Session goal:** Create validated model for GTE G65SC816 - WDC 65C816 second-source

**Starting state:**
- No existing model

**Changes made:**

1. Created initial model with 65C816 native mode timing calibrated for CPI = 3.8
   - alu: 2 cycles (ADC, SBC 16-bit)
   - data_transfer: 3 cycles (LDA, STA 16-bit)
   - memory: 4 cycles (indirect, indexed)
   - control: 3 cycles (BNE, JMP, BRL)
   - stack: 5 cycles (PHA 16-bit, PEA, PEI)
   - long_addr: 5 cycles (24-bit addressing modes)

**What we learned:**
- G65SC816 is GTE's second-source of WDC 65C816
- Full 65816 pinout with 24-bit addressing
- Native mode adds overhead from 16-bit data and long addressing
- Higher CPI than 802 variant due to more use of long addressing
- Bus multiplexing adds overhead for 24-bit address generation

**Final state:**
- CPI: 3.75 (target 3.8, within 5%)
- Validation: PASSED

**References used:**
- WDC 65C816 Data Sheet
- GTE G65SC816 Data Sheet
- Apple IIGS Technical Reference

---
