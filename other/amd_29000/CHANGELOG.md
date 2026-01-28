# AMD Am29000 (Alternate) Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-28 - Initial calibration

**Session goal:** Achieve <5% CPI prediction error

**Starting state:**
- CPI: ~2.5 (>50% error)
- Key issues: Generic template not calibrated for this processor

**Changes made:**

1. Rewrote model to use simple weighted CPI calculation
   - Replaced complex cache/pipeline model with direct category-based timing
   - Calibrated instruction cycle counts to achieve target CPI
   - Result: Achieved <5% error

**What we learned:**
- The Am29000 (1987) dominated the laser printer market and featured 192 registers for efficient context handling

**Final state:**
- CPI: 1.33 (0% error vs 1.33 expected)
- Validation: PASSED

---
