# MOS 8501 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial validation and documentation

**Session goal:** Validate the MOS 8501 grey-box queueing model and create documentation.

**Starting state:**
- Model existed with no validation JSON or documentation files
- Model implements 5 instruction categories (alu, data_transfer, memory, control, stack)
- Target CPI: 3.80

**Changes attempted:**

1. Ran model across all four workloads to collect CPI/IPC results
   - typical: CPI=3.724, IPC=0.269, bottleneck=data_transfer
   - compute: CPI=3.571, IPC=0.280, bottleneck=alu
   - memory: CPI=4.080, IPC=0.245, bottleneck=memory
   - control: CPI=3.819, IPC=0.262, bottleneck=control

2. Created validation JSON with results
3. Created CHANGELOG.md and HANDOFF.md

**What we learned:**
- The MOS 8501 is an HMOS variant of the 6502 used in Commodore C16/Plus4
- Clock speed is 1.76 MHz (PAL timing), approximately 7000 transistors
- Model uses straightforward weighted-average CPI calculation without queueing overhead
- Bottleneck correctly shifts by workload: data_transfer for typical, alu for compute, etc.
- All instruction categories have 2-7 cycle timings consistent with 6502 architecture

**Final state:**
- CPI: 3.724 (2.0% error vs 3.80 target)
- Validation: PASSED

**References used:**
- Model docstring and inline comments referencing 6502 ISA timing (2-7 cycles)
- Commodore C16/Plus4 technical documentation

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 19 evaluations
- Corrections: alu: -0.37, control: +0.27, data_transfer: +1.38, memory: -0.86, stack: -0.93

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
