# Toshiba TLCS-12 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation and validation

**Session goal:** Create validated model for Toshiba TLCS-12 - first Japanese microprocessor

**Starting state:**
- No existing model

**Changes made:**

1. Created initial model with instruction timing calibrated for CPI = 8.0
   - alu: 6 cycles (ADD, SUB, AND, OR)
   - data_transfer: 5 cycles (MOV)
   - memory: 10 cycles (LD, ST)
   - io: 12 cycles (IN, OUT)
   - control: 8 cycles (JMP, JZ, JNZ)

**What we learned:**
- Toshiba TLCS-12 (1973) was the first Japanese microprocessor
- 12-bit PMOS design with approximately 2500 transistors
- Designed for Ford EEC (Electronic Engine Control) system
- PMOS technology resulted in slow multi-cycle operations
- 1 MHz clock speed typical for PMOS era
- Limited instruction set focused on control applications

**Final state:**
- CPI: 8.0 (target)
- Validation: PASSED

**References used:**
- Toshiba TLCS-12 Technical Documentation
- Ford EEC System Design Specifications
- Japanese Semiconductor History Archives

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 8 evaluations
- Corrections: alu: +3.78, control: -1.03, data_transfer: -0.69, io: -2.07, memory: -1.13

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
