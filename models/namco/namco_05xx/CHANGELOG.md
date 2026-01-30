# Namco 05xx Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial creation

**Session goal:** Create Namco 05xx model for starfield generator chip

**Starting state:**
- New model, no previous version

**Changes made:**

1. Created complete processor model
   - 4-bit custom starfield generator architecture
   - 5 instruction categories: star_calc, pixel_out, scroll, control, timing
   - 4 workload profiles: typical, dense_field, scrolling, idle
   - Target CPI: 4.0

**Final state:**
- CPI: 3.7 (7.5% error vs 4.0 expected)
- Validation: PASSED

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 15 evaluations
- Corrections: control: +0.42, pixel_out: -0.46, scroll: -0.16, star_calc: +1.56, timing: -0.62

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
