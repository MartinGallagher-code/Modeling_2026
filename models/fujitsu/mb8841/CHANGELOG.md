# Fujitsu MB8841 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation and validation

**Session goal:** Create validated performance model for Fujitsu MB8841 4-bit MCU

**Starting state:**
- No existing model

**Changes made:**

1. Created MB8841 validated model
   - 5 instruction categories: alu, data_transfer, memory, io, control
   - 4 workload profiles: typical, compute, memory, control
   - Clock: 1 MHz, CPI calibrated to 4.0
   - Modeled for arcade game MCU workloads

2. Created validation JSON with 11 timing tests
   - ALU ops (ADD, SUB, INC): 3 cycles
   - Data transfer (MOV): 3 cycles
   - Memory (LD, ST): 4 cycles
   - I/O (IN, OUT): 6 cycles
   - Control (JMP, CALL, RET): 5 cycles

**What we learned:**
- The MB8841 (1977) is a 4-bit MCU by Fujitsu
- Harvard architecture with 1KB ROM and 32 nibbles RAM
- Used in Namco arcade games: Galaga uses 3 of these chips
- Also used in Xevious and Bosconian
- MAME emulates this as the mb88xx CPU family
- 64 instructions, most 3-5 cycles, I/O operations 6-8 cycles

**Final state:**
- CPI: 4.0 (0.0% error vs 4.0 expected)
- Validation: PASSED

---
