# Intel 8035/8039 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create initial 8039 model based on 8048 timing

**Starting state:**
- No model existed

**Changes made:**

1. Created 8039 model based on Intel 8048 timing
   - The 8035/8039 are ROM-less variants of the MCS-48 family
   - Same instruction set and timing as 8048
   - Calibrated for CPI = 1.5

2. Created validation JSON with timing tests
   - Same instruction timing as 8048
   - Most instructions 1-2 machine cycles

3. Created documentation files

**What we learned:**
- The Intel 8035/8039 (1976) are ROM-less MCS-48 variants
- 8035: 64 bytes RAM, 8039: 128 bytes RAM
- Require external ROM for program storage
- Used in systems requiring flexibility or larger code space
- Same CPU core and timing as 8048

**Final state:**
- CPI: 1.5 (target)
- Validation: PASSED

---
