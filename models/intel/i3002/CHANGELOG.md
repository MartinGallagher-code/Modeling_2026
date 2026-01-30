# Intel 3001/3002 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create initial bit-slice processor model

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model for Intel 3001/3002 bit-slice family
   - Modeled as 2-bit slice ALU with single-cycle microinstructions
   - Target CPI: 1.0 (per micro-op)
   - Clock: 5 MHz typical
   - Based on Schottky bipolar technology

2. Implemented instruction categories
   - alu: ALU operations (ADD, SUB, AND, OR, XOR)
   - shift: Shift operations
   - pass: Data pass-through
   - load: Register load operations
   - All categories execute in 1 cycle

3. Created workload profiles
   - typical, compute, memory, control, mixed

**What we learned:**
- Intel 3002 (1974) was Intel's competitor to the AMD Am2901
- Uses 2-bit slices (vs AMD's 4-bit) requiring more chips for wider data paths
- Part of the 3000 series bit-slice family (3001 MCU, 3002 CPE, 3003 LLC)
- Schottky bipolar technology for high speed
- 11 general-purpose registers per slice

**Final state:**
- CPI: 1.0 (0% error vs 1.0 expected)
- Validation: PASSED

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 4 free correction parameters
- Optimizer converged in 1 evaluations
- Corrections: all near zero (model already matched measurements)

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
