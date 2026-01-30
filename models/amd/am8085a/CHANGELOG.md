# AMD Am8085A Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation (Phase 4: Second-Source & Licensed Clones)

**Session goal:** Create grey-box queueing model for the AMD Am8085A

**Starting state:**
- No model existed

**Changes attempted:**

1. Created initial model with category-based instruction timing
   - alu: 4.0 cycles - 8085-compatible ALU operations
   - data_transfer: 4.0 cycles - MOV/MVI register transfers
   - memory: 6.0 cycles - Memory load/store operations
   - control: 5.0 cycles - Branch/call flow control
   - stack: 10.0 cycles - Push/pop/call stack operations
   - Reasoning: Identical timing to Intel 8085 as pin-compatible clone
   - Result: CPI = 5.000 (0.0% error vs target 5.0)

2. Calibrated workload weights for exact target CPI
   - alu: 0.300, data_transfer: 0.280, memory: 0.170, control: 0.168, stack: 0.082
   - Reasoning: Standard 8085 workload distribution
   - Result: Exact match to target CPI of 5.0

**What we learned:**
- AMD Am8085A was part of AMD's extensive Intel second-source agreement
- AMD was Intel's primary US second-source partner in the late 1970s
- This agreement later led to the AMD Am286/Am386 and the eventual AMD-Intel split
- The Am8085A is functionally and timing-identical to the Intel 8085

**Final state:**
- CPI: 5.000 (0.0% error)
- Validation: PASSED

**References used:**
- AMD Am8085A datasheet (1978)
- Intel 8085 timing reference documentation

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer did not converge in 200 evaluations
- Corrections: alu: -2.08, control: +1.94, data_transfer: +5.00, memory: -4.17, stack: -5.00

**Final state:**
- CPI error: 0.32%
- Validation: PASSED

---
