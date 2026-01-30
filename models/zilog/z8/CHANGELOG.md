# Z8 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-28 - Cross-validation with per-instruction timing tests

**Session goal:** Add comprehensive per-instruction timing tests and cross-validation documentation

**Starting state:**
- CPI: 9.540 (4.60% error)
- Status: PASS

**Changes made:**

1. Added 17 per-instruction timing tests to validation JSON
   - Register ops: LD_r_r, LD_r_Ir, ADD_r_r, INC_r, DEC_r
   - Immediate: LD_r_IM, ADD_r_IM
   - Memory: LD_r_RR, LD_RR_r
   - Control: JP_cc_DA, JR_cc_RA, DJNZ_r_RA, NOP
   - Call/Return: CALL_DA, RET
   - Stack: PUSH, POP

2. Added comprehensive cross_validation section documenting:
   - Register-file architecture notes (144 registers)
   - Z80 comparison (NOT related architecturally)
   - Datasheet comparison methodology
   - Per-instruction accuracy analysis (9/17 passed, 52.9%)
   - Category-weighted accuracy breakdown
   - Workload validation results
   - MCU-specific considerations

**What we learned:**
- Z8 is NOT a Z80 variant - completely different architecture
- Register-file design (144 general-purpose registers)
- Higher CPI than Z80 due to register addressing overhead
- Single-chip MCU design prioritizes integration over raw speed
- Internal clock is half external clock rate

**Final state:**
- CPI: 9.540 (4.60% error) - unchanged
- Validation: PASS
- Per-instruction tests: 17 tests, 52.9% pass rate

**References used:**
- Zilog Z8 Datasheet (ps0199.pdf)
- Z8 Technical Manual (um0016.pdf)

---

## 2026-01-28 - Initial calibration and validation

**Session goal:** Implement validate() method and calibrate model to achieve <5% CPI error

**Starting state:**
- CPI: Unknown (validation pending)
- Key issues: Template model with placeholder timing values, clock speed wrong (1.0 vs 8.0 MHz)

**Changes made:**

1. Updated processor specifications
   - Clock: 1.0 MHz -> 8.0 MHz (correct for Z8)
   - Year: 1980 -> 1979 (correct introduction year)
   - Transistor count: 10000 -> 12000

2. Rewrote instruction categories based on Z8 architecture
   - Parameter: `register_ops` = 6 cycles (LD/ADD/SUB r,r)
   - Parameter: `immediate` = 6 cycles (LD/ADD r,IM)
   - Parameter: `memory` = 12 cycles (indexed/indirect @10-14)
   - Parameter: `control` = 12 cycles (JP/JR/DJNZ)
   - Parameter: `stack` = 14 cycles (PUSH @12-14, POP @10-12)
   - Parameter: `call_return` = 20 cycles (CALL @20, RET @14)

3. Adjusted workload profiles for MCU use cases
   - Typical: 30% register, 20% immediate, 20% memory, 18% control, 7% stack, 5% call/return

4. Implemented validate() method
   - Returns expected_cpi, predicted_cpi, error_percent, validation_passed

**Calibration iterations:**
- First attempt: CPI=8.42 (15.8% error) - cycles too low
- Increased memory, control, stack, call_return cycles
- Final: CPI=9.54 (4.6% error) - PASSED

**What we learned:**
- Z8 uses register-file architecture (144 registers in internal RAM)
- Longer cycle counts than Z80 due to register addressing overhead
- Single-chip MCU design prioritizes integration over raw speed

**Final state:**
- CPI: 9.54 (4.6% error)
- Validation: PASSED

**References used:**
- Z8 architecture documentation
- Comparison with Z80 timings scaled for MCU architecture

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 6 free correction parameters
- Optimizer converged in 2 evaluations
- Corrections: call_return: +10.00, control: -1.49, immediate: -5.00, memory: -1.60, register_ops: +2.37, stack: +7.00

**Final state:**
- CPI error: 3.46%
- Validation: PASSED

---
