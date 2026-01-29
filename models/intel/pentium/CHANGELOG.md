# Intel Pentium Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-28 - Cross-validation with 80x86 family

**Session goal:** Add comprehensive instruction timing tests and cross-validation documentation

**Starting state:**
- CPI: 0.985 (1.5% error)
- Validation: PASSED

**Changes made:**

1. Added 28 per-instruction timing tests to validation JSON
   - ALU: ADD, SUB, CMP, AND, OR, XOR, INC, LEA (1 cycle, pairable UV)
   - Data transfer: MOV variants (1 cycle, pairable UV)
   - Multiply/divide: MUL/DIV 32-bit (11-43 cycles, not pairable)
   - Control: JMP, Jcc (1 cycle predicted, 4 if mispredicted)
   - Memory: PUSH, POP (1 cycle, pairable)
   - FPU: FADD, FMUL, FDIV (3-39 cycles, pipelined)

2. Added cross_validation section documenting:
   - Position as first superscalar x86 processor
   - Predecessor: 80486 (added dual pipeline, branch prediction)
   - Successor: Pentium Pro (out-of-order, 3-wide)
   - Dual pipeline details: U (all instrs), V (simple only)
   - Branch prediction: 256-entry BTB, ~80% accuracy

**What we learned:**
- First x86 to achieve >1 IPC (peak 2 IPC)
- Complex pairing rules limit actual IPC to ~1.0-1.2
- Separate I/D caches (8KB each) reduce structural hazards
- 64-bit external data bus improves memory bandwidth
- Famous FDIV bug led to $475M recall

**Final state:**
- CPI: 0.985 (1.5% error vs expected 1.0)
- Validation: PASSED
- Timing tests: 28 instruction tests added (with pairing info)

---

## 2026-01-28 - Initial calibration

**Session goal:** Achieve <5% CPI prediction error

**Starting state:**
- CPI: uncalibrated (high error)
- Key issues: Model used wrong function signature or uncalibrated template

**Changes made:**

1. Rewrote model to use correct analyze() method
   - Replaced simulate() with analyze() returning AnalysisResult
   - Calibrated instruction cycle counts for target CPI
   - Result: Achieved <5% error

**What we learned:**
- The Intel Pentium (1993) was the first superscalar x86 processor
- 0.8um CMOS technology with 3.1 million transistors, 60 MHz base clock
- Dual pipelines (U and V) can issue 2 instructions per cycle
- Separate I/D caches (8KB each) and dynamic branch prediction

**Final state:**
- CPI: 0.985 (1.5% error vs expected 1.0)
- Validation: PASSED

---
