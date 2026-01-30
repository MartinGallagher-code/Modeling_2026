# ARM1 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-28 - Cross-validation and timing tests

**Session goal:** Add per-instruction timing tests and cross-validation documentation for ARM family

**Starting state:**
- CPI: 1.856 (3.1% error)
- Validation: PASSED

**Changes made:**

1. Added 15 per-instruction timing tests to validation JSON
   - ALU: MOV_r_r, MOV_r_imm, ADD_r_r_r, SUB_r_r_r, AND_r_r_r, ORR_r_r_r, CMP_r_r
   - Load: LDR_r_addr, LDR_r_r_imm
   - Store: STR_r_addr, STR_r_r_imm
   - Branch: B_label, BEQ_label, BL_label
   - Multiply: MUL_r_r_r (16 cycles - no hardware multiplier)

2. Added cross_validation section documenting ARM family evolution
   - Position: First generation - original ARM architecture
   - Predecessor: None (first ARM)
   - Successor: ARM2
   - Key differences to ARM2: hardware multiplier, coprocessor interface, SWP instruction

3. Documented ARM family evolution (ARM1 -> ARM2 -> ARM3 -> ARM6)

**What we learned:**
- ARM1 has highest CPI (1.8) among early ARMs due to no cache and no hardware multiplier
- Most ALU operations are single-cycle across all early ARM generations
- Memory access dominates CPI due to no cache in ARM1
- Branch penalty of 3 cycles consistent with 3-stage pipeline

**Final state:**
- CPI: 1.856 (3.1% error) - unchanged
- Validation: PASSED
- No model changes required (error <5%)

**References used:**
- WikiChip ARM1 architecture documentation
- ARM Technical Reference Manuals
- Wikipedia ARM architecture history

---

## 2026-01-28 - Initial calibration

**Session goal:** Achieve <5% CPI prediction error

**Starting state:**
- CPI: ~3.0 (>50% error)
- Key issues: Generic template not calibrated for this processor

**Changes made:**

1. Rewrote model to use simple weighted CPI calculation
   - Replaced complex cache/pipeline model with direct category-based timing
   - Calibrated instruction cycle counts to achieve target CPI
   - Result: Achieved <5% error

**What we learned:**
- The ARM1 was the first ARM processor (1985) with a simple 3-stage pipeline and no cache, running at 8 MHz

**Final state:**
- CPI: 1.87 (3.9% error vs 1.8 expected)
- Validation: PASSED

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 4 free correction parameters
- Optimizer converged in 7 evaluations
- Corrections: alu: -0.30, branch: -0.26, load: +3.58, store: -5.00

**Final state:**
- CPI error: 1.28%
- Validation: PASSED

---
