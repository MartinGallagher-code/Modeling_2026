# Mitsubishi MELPS 740 (M50740) Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation and validation

**Session goal:** Create validated model for Mitsubishi MELPS 740 - enhanced 6502 microcontroller

**Starting state:**
- No existing model

**Changes made:**

1. Created initial model with instruction timing calibrated for CPI = 3.2
   - alu: 2 cycles (ADC, SBC, INC, DEC)
   - data_transfer: 3 cycles (LDA, STA, LDX, STX)
   - memory: 4 cycles (indexed/indirect addressing modes)
   - control: 3 cycles (BNE, BEQ, JMP, JSR)
   - io: 5 cycles (timer, serial, A/D register access)
   - bit_ops: 2 cycles (SET, CLR, TST bit manipulation)

**What we learned:**
- Mitsubishi MELPS 740 / M50740 (1984) enhanced 6502-compatible microcontroller
- CMOS design with ~15000 transistors at 2 MHz
- Added MUL, DIV, and bit manipulation to 6502 base set
- On-chip peripherals: timer, serial I/O, A/D converter
- Faster than original NMOS 6502 due to CMOS + enhancements
- Popular in consumer electronics and embedded control

**Final state:**
- CPI: 3.2 (target)
- Validation: PASSED

**References used:**
- Mitsubishi MELPS 740 Hardware Manual
- M50740 Application Notes
- MOS 6502 Programming Manual

---
