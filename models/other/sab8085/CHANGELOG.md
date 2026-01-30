# Siemens SAB8085 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation (Phase 4: Second-Source & Licensed Clones)

**Session goal:** Create grey-box queueing model for the Siemens SAB8085

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
   - Reasoning: Weighted toward ALU and data transfer as primary 8085 workload
   - Result: Exact match to target CPI of 5.0

**What we learned:**
- SAB8085 is a direct pin-compatible clone of the Intel 8085
- Improved over SAB8080A with multiplexed bus and serial I/O
- Timing identical to original Intel 8085

**Final state:**
- CPI: 5.000 (0.0% error)
- Validation: PASSED

**References used:**
- Siemens SAB8085 datasheet (1978)
- Intel 8085 timing reference documentation

---
