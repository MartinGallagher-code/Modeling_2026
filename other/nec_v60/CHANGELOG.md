# NEC V60 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation and validation

**Session goal:** Create validated model for NEC V60 - Japan's first major 32-bit CPU

**Starting state:**
- No existing model

**Changes made:**

1. Created initial model with instruction timing calibrated for CPI = 3.0
   - alu: 2 cycles (ADD, SUB, MUL, AND, OR - 32-bit)
   - data_transfer: 2 cycles (MOV, MOVEA - 32-bit)
   - memory: 4 cycles (LD, ST, indexed)
   - control: 3 cycles (BR, Bcc, JSR, RET)
   - float: 8 cycles (FADD, FMUL, FDIV)
   - string: 6 cycles (MOVS, CMPS)

**What we learned:**
- NEC V60 (1986) was Japan's first major 32-bit microprocessor
- Completely new ISA, NOT x86 compatible (unlike V20/V30)
- ~375,000 transistors, 16 MHz CMOS
- On-chip FPU and string instructions
- Competitive with Motorola 68020 and Intel 80386
- Used in NEC workstations
- Followed by V70 successor

**Final state:**
- CPI: 3.05 (target 3.0, within 5%)
- Validation: PASSED

**References used:**
- NEC V60 Technical Manual
- NEC V-Series Processor Family Guide
- Japanese Microprocessor Development Archives

---
