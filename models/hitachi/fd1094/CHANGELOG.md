# Hitachi FD1094 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial creation

**Session goal:** Create FD1094 model for improved encrypted 68000 arcade CPU

**Starting state:**
- New model, no previous version

**Changes made:**

1. Created complete processor model based on FD1089 with improvements
   - Same 68000 core, faster decryption (8 vs 10 cycles)
   - 6 instruction categories: alu, data_transfer, memory, control, address, decrypt
   - 4 workload profiles: typical, compute, memory_heavy, control_heavy
   - Target CPI: 6.8

**Final state:**
- CPI: 6.65 (2.21% error vs 6.8 expected)
- Validation: PASSED

---
