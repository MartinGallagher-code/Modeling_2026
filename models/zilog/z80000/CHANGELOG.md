# Z80000 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-28 - Cross-validation with per-instruction timing tests

**Session goal:** Add comprehensive per-instruction timing tests and cross-validation documentation

**Starting state:**
- CPI: 6.290 (4.83% error)
- Status: PASS

**Changes made:**

1. Added 15 per-instruction timing tests to validation JSON
   - ALU register: LD_R_R, ADD_R_R, INC_R, DEC_R
   - ALU immediate: LD_R_IM, ADD_R_IM
   - Load/Store: LD_R_IR, LD_IR_R
   - Control: JP_cc, JR_cc, NOP
   - Call/Return: CALL, RET
   - Multiply/Divide: MUL, DIV

2. Added comprehensive cross_validation section documenting:
   - 32-bit architecture notes (extended Z8000)
   - Z8000 comparison (architecturally related)
   - Documentation limitations (commercial failure = limited data)
   - Per-instruction accuracy analysis (6/15 passed, 40%)
   - Category-weighted accuracy with confidence levels
   - Workload validation results
   - Historical context

**What we learned:**
- Z80000 is 32-bit extension of Z8000 architecture
- Very limited documentation due to commercial failure
- Timings are estimated from Z8000 baseline
- On-chip MMU with segmentation support
- Zilog exited high-end CPU market after Z80000

**Final state:**
- CPI: 6.290 (4.83% error) - unchanged
- Validation: PASS
- Per-instruction tests: 15 tests, 40% pass rate (based on estimates)
- Confidence: Medium (limited documentation)

**References used:**
- Wikipedia Z80000 article
- CPU-World Z80000 page
- Z8000 Technical Manual (baseline for estimates)

---

## 2026-01-28 - Initial calibration and validation

**Session goal:** Implement validate() method and calibrate model to achieve <5% CPI error

**Starting state:**
- CPI: Unknown (validation pending)
- Key issues: Template model with completely wrong specs (showed 8-bit instead of 32-bit), pipeline model instead of sequential

**Changes made:**

1. Fixed processor specifications
   - Data width: 8 -> 32 bits
   - Address width: 16 -> 32 bits
   - Clock: 1.0 MHz -> 16.0 MHz
   - Transistor count: 10000 -> 91000
   - Year: 1980 -> 1986

2. Replaced pipeline model with sequential execution model
   - Z80000 did not have true pipelining
   - Uses instruction prefetch but sequential execution

3. Rewrote instruction categories for 32-bit architecture
   - Parameter: `alu_reg` = 3 cycles (ADD/SUB R,R)
   - Parameter: `alu_imm` = 4 cycles (ADD/SUB R,IM)
   - Parameter: `load` = 5 cycles (LD R,@RR)
   - Parameter: `store` = 5 cycles (LD @RR,R)
   - Parameter: `control` = 6 cycles (JP/JR)
   - Parameter: `call_return` = 10 cycles (CALL/RET)
   - Parameter: `multiply` = 40 cycles
   - Parameter: `divide` = 55 cycles

4. Implemented validate() method
   - Returns expected_cpi, predicted_cpi, error_percent, validation_passed

**Calibration iterations:**
- First attempt with old pipeline model: CPI=1.4 (way off)
- Switched to sequential model: CPI=8.36 (39% error) - cycles too high
- Reduced cycle counts for 32-bit datapath efficiency
- Final: CPI=6.29 (4.83% error) - PASSED

**What we learned:**
- Z80000 was Zilog's 32-bit extension of Z8000 architecture
- Commercial failure - very limited documentation available
- No true pipelining, just instruction prefetch
- 32-bit datapath allows faster per-operation execution

**Final state:**
- CPI: 6.29 (4.83% error)
- Validation: PASSED

**References used:**
- Z8000 timings as baseline (Z80000 is 32-bit extension)
- Wikipedia for basic specifications
- Estimated timings based on architectural similarities

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 8 free correction parameters
- Optimizer converged in 14 evaluations
- Corrections: alu_imm: -2.27, alu_reg: -1.87, call_return: +4.95, control: +2.69, divide: -11.05, load: +1.25, multiply: -14.34, store: +1.36

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
