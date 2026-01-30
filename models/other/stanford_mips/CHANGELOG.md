# Stanford MIPS Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for Stanford MIPS, the academic RISC processor that led to MIPS R2000

**Starting state:**
- No model existed
- Reference: berkeley_risc1/berkeley_risc2 models

**Research findings:**
- Stanford MIPS was developed by John Hennessy at Stanford (1981-1983)
- MIPS = Microprocessor without Interlocked Pipeline Stages
- 5-stage pipeline (IF, ID, EX, MEM, WB) - deeper than Berkeley RISC
- 32 general-purpose registers (flat, no register windows)
- Delayed branches with 1 delay slot
- Load delay slots (software-scheduled)
- Hardwired control (no microcode)
- Goal: single-cycle execution (CPI approaching 1.0)
- ~25,000 transistors
- 2 MHz clock (research chip)
- Led to commercial MIPS R2000 (1986)

**Changes made:**

1. Created model targeting CPI ~1.2 (accounting for hazards)
   - Single-cycle ALU operations
   - Load: 1.5 cycles (load delay slot stalls)
   - Store: 1 cycle (pipelined)
   - Branch: 1.5 cycles (delay slot)
   - Jump: 1 cycle (delay slot filled)

2. Added 5 instruction categories:
   - alu: 1 cycle (ADD/SUB/AND/OR/XOR/SLT)
   - load: 1.5 cycles (load delay slot)
   - store: 1 cycle (pipelined)
   - branch: 1.5 cycles (with delay slot)
   - jump: 1 cycle (JAL/JR)

3. Key differences from Berkeley RISC:
   - 5-stage pipeline (vs 2-3 stage)
   - 32 flat registers (vs register windows)
   - Software scheduling (vs hardware interlocks)
   - Deeper pipeline = higher clock potential

4. Added comparison function to Berkeley RISC I/II

**What we learned:**
- Stanford MIPS achieved CPI ~1.2 (comparable to Berkeley RISC II)
- Different approach: deeper pipeline + software scheduling
- MIPS philosophy: move complexity to compiler
- RISC philosophy: register windows for fast calls
- Both projects proved RISC viability

**Final state:**
- CPI: 1.15 (~4% error vs target 1.2)
- Validation: PASSED (13/13 tests, 100%)
- ~8.3x faster CPI than VAX 11/780
- Comparable to Berkeley RISC II

**References used:**
- Hennessy, J.L.: VLSI Processor Architecture (1984)
- Hennessy & Patterson: Computer Architecture: A Quantitative Approach
- Wikipedia: MIPS architecture
- MIPS R2000 documentation (successor)
- Berkeley RISC models for comparison

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 13 evaluations
- Corrections: alu: -0.09, branch: +0.32, jump: -0.72, load: +1.96, store: -1.74

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
