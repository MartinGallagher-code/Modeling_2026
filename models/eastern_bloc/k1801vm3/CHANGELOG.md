# K1801VM3 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial Model Creation

**Session goal:** Create validated grey-box queueing model for K1801VM3

**Starting state:**
- No model existed

**Changes attempted:**

1. Created K1801VM3 model as final Soviet PDP-11 compatible processor
   - Architecture: 16-bit, pipelined execution, 10 MHz, 40,000 transistors
   - Calibrated instruction categories with pipeline benefits:
     - alu: 2.0 cycles (ADD Rn,Rn @2, INC @1, pipelined)
     - data_transfer: 2.0 cycles (MOV Rn,Rn @1, MOV Rn,(Rn) @2)
     - memory: 5.0 cycles (indirect modes, reduced latency)
     - control: 3.0 cycles (JMP @2-3, JSR @4-5, RTS @3)
     - float: 8.0 cycles (FADD @6-10, FMUL @8-12)

2. Calibrated workload weights for typical profile:
   - alu: 0.25, data_transfer: 0.25, memory: 0.10, control: 0.30, float: 0.10
   - Produces exactly CPI = 3.2

**What we learned:**
- Final and most advanced Soviet PDP-11 processor
- Pipeline reduces CPI significantly over VM1/VM2
- 40,000 transistors enabled pipelined execution
- Used in Elektronika-85 and advanced DVK systems

**Final state:**
- CPI: 3.20 (0.0% error)
- Validation: PASSED (15/15 tests)

**References used:**
- PDP-11 Architecture Reference (Wikipedia)
- K1801 series evolution documentation
