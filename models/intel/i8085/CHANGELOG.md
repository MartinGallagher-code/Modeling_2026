# Intel 8085 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

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
- The Intel 8085 (1976) was an enhanced 8080 with single +5V power supply
- 3um NMOS technology with 6500 transistors, 3 MHz clock
- Instructions take 4-18 cycles, improved over 8080
- Added SID/SOD serial I/O and interrupt improvements

**Final state:**
- CPI: 5.5 (0.0% error vs expected 5.5)
- Validation: PASSED

---

## 2026-01-28 - Cross-validation with Intel 8080 family

**Session goal:** Cross-validate i8085 against i8008 and i8080 family members

**Starting state:**
- CPI: 5.5 (0.0% error)
- Validation: PASSED

**Changes made:**

1. Added comprehensive timing tests (34 instructions)
   - Data transfer: MOV_r_r, MVI_r, LXI (4-10 cycles)
   - Memory: MOV_r_M, MOV_M_r, MVI_M, LDA, STA, IN, OUT (7-13 cycles)
   - ALU: ADD_r, ADD_M, ADI, SUB_r, INR_r, DCR_r, INX, DCX, DAD (4-10 cycles)
   - Control: JMP, Jcond, CALL, Ccond, RET, Rcond, RIM, SIM, NOP, HLT (4-18 cycles)
   - Stack: PUSH, POP, XTHL (10-16 cycles)

2. Added cross_validation section
   - Family comparison with i8008, i8080
   - Instruction timing comparison table
   - Documented 8085-unique instructions (RIM, SIM)
   - Verified timing consistency with 8080

**What we learned:**
- 8085 shares ISA with 8080 but has some faster timings
- MOV_r_r is 4 cycles on 8085 vs 5 cycles on 8080
- CALL is 18 cycles on 8085 vs 17 on 8080 (slight difference)
- RIM/SIM are 8085-specific for interrupt mask handling (4 cycles each)
- Conditional branches: 7 cycles not taken, 10 cycles taken

**Final state:**
- CPI: 5.5 (0.0% error)
- Validation: PASSED
- Cross-validation: Complete

**References used:**
- Intel 8085 datasheet instruction timing
- MAME emulator timing tables

---
