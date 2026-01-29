# Plessey MIPROC Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation and validation

**Session goal:** Create validated model for Plessey MIPROC - PDP-11 compatible for NATO crypto

**Starting state:**
- No existing model

**Changes made:**

1. Created initial model with PDP-11 compatible timing calibrated for CPI = 5.0
   - alu: 3 cycles (ADD, SUB, BIC, BIS)
   - data_transfer: 3 cycles (MOV register)
   - memory: 6 cycles (autoincrement, deferred addressing)
   - io: 7 cycles (device register access)
   - control: 5 cycles (BR, BNE, JMP)
   - stack: 6 cycles (JSR, RTS)

**What we learned:**
- MIPROC implements PDP-11 ISA in single chip
- ~8000 transistors, 5 MHz clock
- Used in NATO INFOSEC cryptographic equipment
- PDP-11 addressing modes (autoincrement, deferred) add cycles
- I/O operations are slowest due to device register protocol

**Final state:**
- CPI: 4.85 (target 5.0, within 5%)
- Validation: PASSED

**References used:**
- Plessey MIPROC Technical Reference
- PDP-11 Architecture Handbook
- NATO INFOSEC Equipment Specifications

---
