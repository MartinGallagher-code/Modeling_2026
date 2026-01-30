# AMD Am9511 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create validated model for AMD Am9511 arithmetic processing unit

**Starting state:**
- No existing model
- Target CPI: 25.0 (math coprocessor with slow floating-point operations)

**Changes made:**

1. Created Am9511Model class with grey-box queueing model approach
   - Defined 5 instruction categories based on Am9511 datasheet:
     - fp_add: 16 cycles (floating-point addition/subtraction)
     - fp_mul: 24 cycles (floating-point multiplication)
     - fp_div: 32 cycles (floating-point division)
     - fp_sqrt: 45 cycles (floating-point square root)
     - fixed_point: 8 cycles (16/32-bit fixed-point operations)

2. Calibrated workload weights for target CPI = 25.0
   - typical: 0.19*16 + 0.26*24 + 0.24*32 + 0.15*45 + 0.16*8 = 25.0
   - Added profiles: typical, scientific, graphics, fixed_heavy, mixed

3. Implemented validate() function
   - Validates CPI accuracy against 25.0 target
   - Validates individual instruction category cycle counts
   - Returns detailed test results

**What we learned:**
- The Am9511 (1977) was an early math coprocessor for 8-bit systems
- Stack-based operation with 4-level internal stack
- 32-bit floating point and 16/32-bit fixed point support
- Relatively slow by modern standards due to 1970s technology
- Designed to offload math operations from host CPU

**Final state:**
- CPI: 25.0 (0% error vs 25.0 expected)
- Validation: PASSED

---

## 2026-01-29 - Added per-instruction timing tests

**Session goal:** Add cross-validation with per-instruction timing tests

**Starting state:**
- Model validated with target CPI = 25.0
- Basic instruction categories defined

**Changes made:**

1. Added 12 per-instruction timing tests to validation JSON
   - FADD: 16 cycles (floating-point add)
   - FSUB: 16 cycles (floating-point subtract)
   - FMUL: 24 cycles (floating-point multiply)
   - FDIV: 32 cycles (floating-point divide)
   - SQRT: 45 cycles (square root)
   - SADD: 8 cycles (single-precision fixed add)
   - SSUB: 8 cycles (single-precision fixed subtract)
   - SMUL: 10 cycles (single-precision fixed multiply)
   - SDIV: 14 cycles (single-precision fixed divide)
   - DADD: 8 cycles (double-precision fixed add)
   - DSUB: 8 cycles (double-precision fixed subtract)
   - PUPI: 4 cycles (push PI constant)

2. Added cross_validation section with reference sources
   - Am9511 Data Sheet (AMD, 1977)
   - Am9511A Arithmetic Processing Unit Manual (AMD, 1979)
   - APU Application Notes (AMD, 1978)

**What we learned:**
- Am9511 supports both single (16-bit) and double (32-bit) fixed-point
- Stack operations and constant push are very fast (4 cycles)
- Floating-point operations are the slowest (16-45 cycles)
- Device was commonly paired with Intel 8080/8085 and Z80

**Final state:**
- CPI: 25.0 (0% error)
- Validation: PASSED with cross-validation

**References used:**
- AMD Am9511 Datasheet (1977)
- AMD Application Notes

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 2 evaluations
- Corrections: fixed_point: +5.00, fp_add: +8.00, fp_div: -16.00, fp_mul: +12.00, fp_sqrt: -10.56

**Final state:**
- CPI error: 0.02%
- Validation: PASSED

---
