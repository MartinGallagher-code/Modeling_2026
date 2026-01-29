# Berkeley RISC I Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-28 - Initial model creation

**Session goal:** Create grey-box queueing model for the first RISC processor

**Starting state:**
- No model existed

**Research findings:**
- Berkeley RISC I was the first RISC processor (UC Berkeley, 1982)
- 2-stage pipeline (fetch/decode + execute)
- Most ALU instructions: 1 cycle
- Load/store instructions: 2 cycles
- 78 registers with 6 overlapping windows
- Delayed branches (branch delay slot)
- 31 total instructions
- 44,500 transistors in 2-4 micron NMOS
- 4 MHz clock

**Changes made:**

1. Created model targeting CPI ~1.3 (near single-cycle)
   - Most operations single-cycle
   - Only memory operations take 2 cycles
   - Delayed branches effectively hide branch latency

2. Added 5 instruction categories:
   - alu: 1 cycle (ADD/SUB/AND/OR)
   - load: 2 cycles (memory access)
   - store: 2 cycles (memory access)
   - branch: 1 cycle (delay slot filled)
   - call: 1 cycle (register window switch)

3. Key RISC I innovations modeled:
   - Register windows eliminate most call/return overhead
   - Load/store architecture - only memory ops touch memory
   - Delayed branches hide branch penalty

**What we learned:**
- RISC I achieved CPI ~1.3 (vs VAX 11/780's ~10)
- Register windows were key to fast procedure calls
- The simple pipeline made high clock speeds achievable
- Direct influence on Sun SPARC and ARM architectures

**Final state:**
- CPI: 1.30 (0.0% error vs target 1.3)
- Validation: PASSED
- ~7.7x faster CPI than VAX 11/780

**References used:**
- Patterson & Sequin: RISC I Technical Report (1982)
- Design and Implementation of RISC I (UC Berkeley EECS)
- Wikipedia: Berkeley RISC
- The SPARC Architecture Manual

---
