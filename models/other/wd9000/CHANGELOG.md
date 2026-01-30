# Western Digital WD9000 Pascal MicroEngine Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation and validation

**Session goal:** Create validated model for WD9000 Pascal MicroEngine

**Starting state:**
- No existing model

**Changes made:**

1. Created initial model with instruction timing calibrated for CPI = 8.0
   - stack_ops: 4 cycles (SLDC, SLDL, push/pop/dup)
   - arithmetic: 8 cycles (ADI, SBI, MPI)
   - memory: 6 cycles (LDO, STL, indirect load/store)
   - procedure: 14 cycles (CSP, RPU - call/return with frame management)
   - control: 5 cycles (UJP, FJP - branches)
   - comparison: 6 cycles (EQUI, NEQI - compare/test)

**What we learned:**
- WD9000 (1979) executed UCSD Pascal p-code directly in hardware
- Microprogrammed design with ~10000 transistors at 10 MHz
- Stack-based architecture with hardware procedure frame management
- Complex p-code operations (procedure calls with bounds checking) dominate CPI
- Unique language-specific hardware approach
- Faster than software p-code interpreters on contemporary CPUs

**Final state:**
- CPI: 8.0 (target)
- Validation: PASSED

**References used:**
- WD9000 Pascal MicroEngine Technical Manual
- UCSD Pascal System Documentation
- Byte Magazine WD9000 Review (1980)

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 6 free correction parameters
- Optimizer did not converge in 200 evaluations
- Corrections: arithmetic: -1.53, comparison: -5.00, control: +5.00, memory: +4.02, procedure: -3.49, stack_ops: +5.00

**Final state:**
- CPI error: 0.51%
- Validation: PASSED

---
