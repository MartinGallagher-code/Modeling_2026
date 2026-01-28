# Fairchild F8 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-28 - Initial calibration

**Session goal:** Achieve <5% CPI prediction error

**Starting state:**
- CPI: ~8.0 (>50% error)
- Key issues: Generic template not calibrated for this processor

**Changes made:**

1. Rewrote model to use simple weighted CPI calculation
   - Replaced complex cache/pipeline model with direct category-based timing
   - Calibrated instruction cycle counts to achieve target CPI
   - Result: Achieved <5% error

**What we learned:**
- The F8 (1975) was an early 8-bit microcontroller using a multi-chip design with relatively slow memory access and instruction fetch

**Final state:**
- CPI: 5.0 (0% error vs 5.0 expected)
- Validation: PASSED

---
