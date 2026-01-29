# Mitsubishi MELPS 4 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for Mitsubishi MELPS 4

**Starting state:**
- No model existed

**Research findings:**
- MELPS 4 (M58840) was Mitsubishi's first 4-bit MCU (1978)
- PMOS technology, 400 kHz clock
- Variable instruction timing: 4-8 cycles
- Used in consumer electronics and appliances

**Changes made:**
1. Created model with variable timing: alu@4, data_transfer@5, memory@7, io@8, control@6
2. Added 5 workload profiles
3. Added validation tests for CPI, weight sums, cycle ranges

**Final state:**
- CPI: 6.0 (target met)
- Validation: PASSED

---
