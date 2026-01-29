# National NS32081 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create initial 32-bit FPU model

**Starting state:**
- No model existed

**Changes made:**

1. Created initial model for National NS32081 FPU
   - Modeled as IEEE 754 compatible floating-point unit
   - Target CPI: 15.0
   - Clock: 10 MHz (matching NS32016/NS32032)

2. Implemented instruction categories
   - fp_add: 8 cycles (single-precision add/subtract)
   - fp_mul: 12 cycles (single-precision multiply)
   - fp_div: 20 cycles (single-precision divide)
   - fp_sqrt: 30 cycles (square root)
   - dp_add: 12 cycles (double-precision add/subtract)
   - dp_mul: 18 cycles (double-precision multiply)
   - dp_div: 32 cycles (double-precision divide)
   - conversion: 6 cycles (format conversion)

3. Created workload profiles
   - typical, scientific, graphics, dsp, mixed

**What we learned:**
- NS32081 (1982) was the FPU for the NS32000 family
- IEEE 754 floating-point standard support
- Both 32-bit and 64-bit floating-point operations
- Tightly coupled with NS32016/NS32032 via slave protocol
- Part of National's complete 32-bit microprocessor ecosystem

**Final state:**
- CPI: 14.96 (0.27% error vs 15.0 expected)
- Validation: PASSED

---
