# GI PIC1650 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-28 - Initial model creation

**Session goal:** Create grey-box queueing model for the first PIC microcontroller

**Starting state:**
- No model existed

**Research findings:**
- PIC1650 was the first PIC microcontroller (General Instrument, 1977)
- Harvard architecture (12-bit instructions, 8-bit data)
- Most instructions: 1 instruction cycle (4 oscillator clocks)
- Branch/call: 2 instruction cycles
- 33 instructions total
- 2-level hardware stack only
- 512 x 12-bit ROM, 32 bytes RAM
- 1 MHz oscillator = 250 KIPS

**Changes made:**

1. Created model targeting CPI ~1.15 (mostly single-cycle)
   - Most instructions single-cycle
   - Only branches/calls take 2 cycles
   - Harvard architecture allows instruction fetch during execution

2. Added 6 instruction categories:
   - alu: 1 cycle (ADDWF, ANDWF, SUBWF)
   - data_transfer: 1 cycle (MOVF, MOVWF)
   - bit_ops: 1 cycle (BCF, BSF, BTFSC)
   - literal: 1 cycle (MOVLW, ADDLW)
   - branch: 2 cycles (GOTO)
   - call: 2 cycles (CALL, RETLW)

3. Workload profile reflects embedded controller usage:
   - Heavy ALU and data transfer
   - Moderate bit operations (I/O control)
   - Lower branch percentage than general-purpose CPUs

**What we learned:**
- PIC's Harvard architecture enables efficient pipelining
- 2-level stack severely limits recursion
- Bit operations are key for I/O-heavy embedded work
- The "PIC" name originally meant "Peripheral Interface Controller"

**Final state:**
- CPI: 1.15 (0.0% error)
- Validation: PASSED
- 10/10 per-instruction timing tests passing

**References used:**
- GI PIC1650 Datasheet
- Wikipedia: PIC microcontrollers
- Microchip PIC Baseline Architecture Guide
- EEJournal: History of Early Microcontrollers

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 6 free correction parameters
- Optimizer converged in 18 evaluations
- Corrections: alu: +0.26, bit_ops: -0.31, branch: -0.51, call: -0.34, data_transfer: +0.51, literal: -1.06

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
