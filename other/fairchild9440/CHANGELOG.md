# Fairchild 9440 MICROFLAME Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation and validation

**Session goal:** Create validated performance model for Fairchild 9440 MICROFLAME

**Starting state:**
- No existing model

**Changes made:**

1. Created Fairchild 9440 validated model
   - 6 instruction categories: alu @2, data_transfer @2, memory @4, io @6, control @3, stack @5
   - 4 workload profiles: typical, compute, memory, control
   - Clock: 10 MHz, CPI calibrated to 3.5
   - I2L bipolar process for fast register operations

2. Created validation JSON with 13 timing tests
   - ALU (ADD, SUB, COM, NEG): 2 cycles
   - Data transfer (MOV): 2 cycles
   - Memory (LDA, STA, ISZ): 4 cycles
   - I/O (DIA, DOA): 6 cycles
   - Control (JMP): 3 cycles
   - Stack (JSR, RET): 5 cycles

**What we learned:**
- The Fairchild 9440 (1979) implemented the Data General Nova ISA on a single chip
- Used I2L (Integrated Injection Logic) bipolar process
- ~5000 transistors, 10 MHz clock
- Faster than original Nova minicomputer
- 4 accumulators (AC0-AC3), 16-bit operations
- Nova ISA has no hardware stack - JSR saves return address in AC3
- Register operations are fast (2 cycles) vs memory (4 cycles)

**Final state:**
- CPI: 3.5 for typical workload
- Validation: PASSED

---
