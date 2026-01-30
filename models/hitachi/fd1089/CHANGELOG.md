# Hitachi FD1089 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial creation

**Session goal:** Create FD1089 model for encrypted 68000 arcade CPU

**Starting state:**
- New model, no previous version

**Changes made:**

1. Created complete processor model
   - 68000 core with decryption overlay
   - 6 instruction categories: alu, data_transfer, memory, control, address, decrypt
   - 4 workload profiles: typical, compute, memory_heavy, control_heavy
   - Target CPI: 7.0

2. Key design decisions:
   - Decrypt category models the per-instruction decryption overhead
   - Base timing from 68000 datasheet with measured decrypt penalty
   - CPI higher than standard 68000 due to opcode decryption

**Final state:**
- CPI: 6.85 (2.14% error vs 7.0 expected)
- Validation: PASSED

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 6 free correction parameters
- Optimizer converged in 168 evaluations
- Corrections: address: -5.00, alu: -2.64, control: -1.05, data_transfer: +5.00, decrypt: +5.00, memory: +1.21

**Final state:**
- CPI error: 1.07%
- Validation: PASSED

---
