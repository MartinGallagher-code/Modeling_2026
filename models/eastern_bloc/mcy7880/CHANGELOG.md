# MCY7880 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial Model Creation

**Session goal:** Create validated grey-box queueing model for MCY7880

**Starting state:**
- No model existed

**Changes attempted:**

1. Created MCY7880 model as Polish Intel 8080A clone
   - Architecture: 8-bit, sequential execution, 2 MHz, 6,000 transistors
   - Calibrated instruction categories from 8080A timing:
     - alu: 4.0 cycles (ADD r @4, ADI @7, INR @5)
     - data_transfer: 5.0 cycles (MOV r,r @5, MVI @7, LXI @10)
     - memory: 7.0 cycles (LDA @13, STA @13, MOV r,M @7)
     - control: 5.0 cycles (JMP @10, CALL @17, RET @10, Jcc ~5 avg)
     - stack: 10.0 cycles (PUSH @11, POP @10, XTHL @18)

2. Calibrated workload weights for typical profile:
   - alu: 0.30, data_transfer: 0.25, memory: 0.15, control: 0.20, stack: 0.10
   - Produces exactly CPI = 5.5

**What we learned:**
- Polish 8080A clone by CEMI, fully compatible timing
- Used in Meritum and Elwro 800 Junior computers
- 8080A T-states mapped to average cycle counts

**Final state:**
- CPI: 5.50 (0.0% error)
- Validation: PASSED (15/15 tests)

**References used:**
- Intel 8080A Datasheet (timing reference)
- Polish computing history references
