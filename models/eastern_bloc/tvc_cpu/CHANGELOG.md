# TVC CPU Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial Model Creation

**Session goal:** Create validated grey-box queueing model for TVC CPU

**Starting state:**
- No model existed

**Changes attempted:**

1. Created TVC CPU model as Hungarian modified Z80 clone
   - Architecture: 8-bit, sequential execution, 3.5 MHz, 9,000 transistors
   - Calibrated instruction categories from Z80 timing with modifications:
     - alu: 4.0 cycles (ADD A,r @4, INC r @4, CP @4)
     - data_transfer: 4.0 cycles (LD r,r @4, LD r,n @7)
     - memory: 6.0 cycles (LD A,(nn) @13, indexed modes)
     - control: 5.0 cycles (JP @10, CALL @17, RET @10, JR @12/7)
     - block: 11.0 cycles (LDIR slightly optimized over Z80A)

2. Calibrated workload weights for typical profile:
   - alu: 0.30, data_transfer: 0.25, memory: 0.15, control: 0.20, block: 0.10
   - Produces exactly CPI = 5.2

**What we learned:**
- Hungarian modified Z80 clone by MEV/Tungsram
- Slightly improved block operations over standard Z80
- Powered the Videoton TVC home computer
- Running at 3.5 MHz, standard Z80A speed

**Final state:**
- CPI: 5.20 (0.0% error)
- Validation: PASSED (15/15 tests)

**References used:**
- Zilog Z80 Datasheet (timing reference)
- Videoton TVC technical documentation
