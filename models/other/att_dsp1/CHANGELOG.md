# AT&T DSP-1 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create initial validated model for AT&T DSP-1 early Bell Labs DSP

**Starting state:**
- New model, no previous implementation

**Changes made:**

1. Created grey-box queueing model with weighted CPI calculation
   - Implemented instruction categories: mac, alu, data_move, control, io
   - Calibrated for target CPI of 4.0 (early microcoded DSP)
   - Created workload profiles for typical, compute, control, io_heavy, mixed

2. Key calibration decisions:
   - MAC: 3 cycles (no hardware MAC, software multiply-accumulate)
   - ALU: 3 cycles (microcoded operations)
   - Data move: 3 cycles (basic data transfers)
   - Control: 5 cycles (branch/jump overhead)
   - I/O: 6 cycles (peripheral interface)

**What we learned:**
- The DSP-1 was one of the earliest DSP designs (1980)
- Captive Bell Labs use only, never commercially available
- Microcoded architecture resulted in high CPI
- Predecessor to the DSP-20 and later WE DSP series

**Final state:**
- CPI: 3.95 (1.25% error vs 4.0 expected)
- Validation: PASSED

---
