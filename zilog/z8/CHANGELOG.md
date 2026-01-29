# Z8 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

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
