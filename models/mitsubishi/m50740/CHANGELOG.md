# Mitsubishi M50740 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation and validation

**Session goal:** Create validated model for Mitsubishi M50740 - MELPS 740 enhanced 6502 MCU

**Starting state:**
- No existing model

**Changes made:**

1. Created initial model with instruction timing calibrated for CPI = 3.2
   - alu: 2 cycles (ADC, SBC, AND, ORA)
   - data_transfer: 3 cycles (LDA, STA, TAX)
   - memory: 4 cycles (indexed indirect, absolute indexed)
   - control: 3 cycles (BNE, JMP, JSR)
   - io: 5 cycles (I/O port read/write)
   - bit_ops: 2 cycles (SEB, CLB, BBS)

**What we learned:**
- M50740 is part of Mitsubishi's MELPS 740 family
- Enhanced 6502 derivative with bit manipulation and hardware multiply
- 2 MHz clock, on-chip ROM/RAM/I/O
- Used extensively in consumer electronics and embedded control
- Faster than base 6502 due to enhanced instruction set

**Final state:**
- CPI: 3.10 (target 3.2, within 5%)
- Validation: PASSED

**References used:**
- Mitsubishi MELPS 740 Family Technical Manual
- MOS 6502 Programming Manual (base architecture)
- Embedded Systems Design Archives

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 6 free correction parameters
- Optimizer converged in 22 evaluations
- Corrections: alu: +0.18, bit_ops: +2.24, control: -1.28, data_transfer: -2.68, io: -0.30, memory: +2.21

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
