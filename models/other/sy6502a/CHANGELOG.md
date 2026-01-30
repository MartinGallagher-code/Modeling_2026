# Synertek SY6502A Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create Synertek SY6502A model based on MOS 6502

**Starting state:**
- No existing model

**Changes made:**

1. Created complete model based on MOS 6502:
   - Identical instruction set and timing to 6502
   - Instruction categories: alu, data_transfer, memory, control, stack
   - Target CPI: 3.0 (cross-validated from 6502)

2. Documented SY6502A-specific features:
   - Licensed 6502 from Synertek
   - Speed-binned for 2 MHz operation (vs 1 MHz for standard 6502)
   - Same die and transistor count as MOS 6502 (3510)
   - "A" suffix indicates higher speed grade

3. Key difference from MOS 6502:
   - Higher clock speed (2 MHz vs 1 MHz)
   - Results in ~652,000 IPS vs ~326,000 IPS

4. Validation tests include:
   - CPI accuracy (target 3.0)
   - Workload weight sums
   - Cycle count ranges
   - IPC range
   - SY6502A-specific: clock speed (2.0 MHz), higher IPS

**Final state:**
- CPI: 3.065 (2.17% error vs target 3.0)
- IPS: ~652,000 at 2 MHz
- All validation tests passing
- Model consistent with MOS 6502 timing

**References used:**
- MOS Technology 6502 Datasheet (May 1976)
- MOS 6502 model (this project)
- Synertek SY6502A datasheet

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 21 evaluations
- Corrections: alu: -0.62, control: +0.63, data_transfer: +1.91, memory: -1.24, stack: +0.51

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
