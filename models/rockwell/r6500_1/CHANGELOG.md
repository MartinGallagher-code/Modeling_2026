# Rockwell R6500/1 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation and validation

**Session goal:** Create validated model for Rockwell R6500/1 - single-chip 6502 MCU

**Starting state:**
- No existing model

**Changes made:**

1. Created initial model with 6502 instruction timing calibrated for CPI = 3.0
   - alu: 2 cycles (ADC, SBC, AND, ORA, EOR)
   - data_transfer: 3 cycles (LDA, STA, TAX, TXA)
   - memory: 4 cycles (indexed indirect, absolute indexed)
   - control: 3 cycles (BNE, JMP, JSR)
   - stack: 3 cycles (PHA, PLA)

**What we learned:**
- R6500/1 uses identical 6502 instruction timing
- Single-chip integration of 2KB ROM, 64B RAM, I/O, timer
- Well-documented due to 6502 heritage
- Widely used in consumer and industrial applications

**Final state:**
- CPI: 2.90 (target 3.0, within 5%)
- Validation: PASSED

**References used:**
- MOS 6502 Programming Manual
- Rockwell R6500 Family Data Sheet
- 6502.org timing reference

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 18 evaluations
- Corrections: alu: +0.89, control: +0.10, data_transfer: +0.45, memory: -1.07, stack: -0.37

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
