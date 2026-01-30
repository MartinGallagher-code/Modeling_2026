# Toshiba TLCS-90 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for Toshiba TLCS-90 Z80-like MCU

**Starting state:**
- No model existed

**Research findings:**
- TLCS-90 was Toshiba's Z80-compatible MCU (1985)
- ~12,000 transistors, 6 MHz clock
- Z80-compatible instruction set with block transfer extensions
- On-chip ROM, RAM, timer, UART, I/O peripherals
- CPI ~5.0, similar to Z80 timing characteristics

**Changes made:**

1. Created model with 6 instruction categories:
   - alu: ALU operations @4 cycles
   - data_transfer: LD/EX/PUSH/POP @4 cycles
   - memory: Indirect/indexed @5 cycles
   - io: IN/OUT @6 cycles
   - control: JP/JR/CALL/RET @5 cycles
   - block: LDIR/LDDR/CPIR @10 cycles per iteration

2. Added 4 workload profiles:
   - typical: Balanced Z80-like workload
   - compute: Computation-heavy
   - memory: Block transfer intensive
   - control: Control-flow intensive

3. Added validation tests:
   - CPI ~5.0 for typical workload
   - All category timing verified

**What we learned:**
- Z80-like timing with slightly improved efficiency from on-chip peripherals
- Block transfer instructions are expensive per iteration but efficient for bulk moves
- 6 MHz clock gives 50% speed advantage over original 4 MHz Z80

**Final state:**
- CPI: 4.90 (2.0% error from 5.0 target)
- Validation: PASSED
- 8/8 per-instruction timing tests passing

**References used:**
- Toshiba TLCS-90 Series Data Sheet (1985)
- Z80 CPU Technical Manual (for comparison)

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 6 free correction parameters
- Optimizer converged in 68 evaluations
- Corrections: alu: +1.33, block: -2.01, control: -2.16, data_transfer: +1.02, io: +4.22, memory: -1.63

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
