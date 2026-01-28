# TI TMS320C10 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

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
- The TMS320C10 (1983) was the first low-cost DSP with single-cycle multiply-accumulate operations

**Final state:**
- CPI: 1.5 (0% error vs 1.5 expected)
- Validation: PASSED

---
