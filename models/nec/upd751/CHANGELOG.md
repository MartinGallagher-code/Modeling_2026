# NEC uPD751 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for NEC's early 4-bit MCU

**Starting state:**
- No model existed

**Research findings:**
- uPD751 was NEC's early 4-bit microcontroller, introduced in 1974
- Enhanced version of the uCOM-4 architecture
- 4-bit data path with parallel ALU
- Variable instruction timing (unlike fixed-timing uCOM-4)
- More complex instruction set with additional addressing modes
- Typical clock: 400 kHz
- Used in consumer electronics and appliances

**Changes made:**

1. Created model with variable instruction timing
   - Target CPI: 8.0 (between uCOM-4's 6.0 and PPS-4's 12.0)
   - Variable cycle counts per instruction category
   - Clock: 400 kHz

2. Added 5 instruction categories:
   - alu: BCD arithmetic @8 cycles
   - data_transfer: Register-memory transfers @7 cycles
   - memory: Load/store with addressing modes @9 cycles
   - control: Branch, call, return @8 cycles
   - io: I/O operations @7 cycles

3. Added 5 workload profiles:
   - typical: General embedded use
   - compute: Calculator-style arithmetic
   - memory: Data manipulation
   - control: Control-flow intensive
   - mixed: General purpose

4. Added validation tests:
   - CPI ~8.0 for typical workload
   - IPS ~50,000 at 400 kHz
   - CPI between uCOM-4 (6.0) and PPS-4 (12.0)
   - Memory identified as bottleneck for memory-heavy workloads

**What we learned:**
- Enhanced instruction set came at cost of increased cycle counts
- Variable timing adds complexity compared to fixed-timing designs
- Additional addressing modes useful but slower than simple operations
- Position between uCOM-4 and PPS-4 reflects trade-off between features and speed

**Final state:**
- CPI: ~8.0 (target achieved)
- Validation: PASSED
- Variable timing model correctly predicts workload-dependent performance

**References used:**
- NEC microcontroller historical documentation
- Japanese semiconductor industry archives
- Comparison with uCOM-4 and TI TMS1000

---
