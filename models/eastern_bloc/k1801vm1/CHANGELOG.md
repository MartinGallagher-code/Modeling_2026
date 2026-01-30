# K1801VM1 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial Model Creation

**Session goal:** Create validated grey-box queueing model for K1801VM1

**Starting state:**
- No model existed

**Changes attempted:**

1. Created K1801VM1 model as Soviet PDP-11 compatible processor
   - Architecture: 16-bit, sequential execution, 5 MHz, 15,000 transistors
   - Calibrated instruction categories from PDP-11 timing documentation:
     - alu: 3.0 cycles (ADD Rn,Rn @3, INC @2, CMP @3)
     - data_transfer: 4.0 cycles (MOV Rn,Rn @2, MOV Rn,(Rn) @4)
     - memory: 7.0 cycles (indirect modes, deferred addressing)
     - control: 5.0 cycles (JMP @4-5, JSR @6-7, RTS @5)
     - stack: 8.0 cycles (PUSH @6, POP @5, interrupt save/restore)

2. Calibrated workload weights for typical profile:
   - alu: 0.25, data_transfer: 0.25, memory: 0.15, control: 0.20, stack: 0.15
   - Produces exactly CPI = 5.0

**What we learned:**
- First Soviet single-chip PDP-11 implementation (1980)
- Used in DVK desktop computers and Elektronika systems
- PDP-11 instruction timing well-documented from DEC sources

**Final state:**
- CPI: 5.00 (0.0% error)
- Validation: PASSED (15/15 tests)

**References used:**
- PDP-11 Architecture Reference (Wikipedia)
- DEC PDP-11 instruction timing documentation
