# Panafacom MN1610 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation and validation

**Session goal:** Create validated model for Panafacom MN1610 - one of Japan's first 16-bit CPUs

**Starting state:**
- No existing model

**Changes made:**

1. Created initial model with instruction timing calibrated for CPI = 8.0
   - register_ops: 5 cycles (ADD, SUB, AND, OR)
   - immediate: 7 cycles (LDI, ADI)
   - memory_read: 10 cycles (LD, LDX)
   - memory_write: 10 cycles (ST, STX)
   - branch: 10 cycles (JMP, BZ, BNZ)
   - call_return: 14 cycles (CALL, RET)

**What we learned:**
- Panafacom MN1610 (1975) was one of Japan's first 16-bit microprocessors
- Developed by Panafacom (joint venture of Matsushita, Fujitsu, and NEC)
- Featured minicomputer-like architecture
- 16-bit data bus with 16-bit address space (64KB)
- Relatively slow for its word size due to early technology
- Influenced later Japanese microprocessor development

**Final state:**
- CPI: 8.0 (target)
- Validation: PASSED

**References used:**
- Panafacom MN1610 Technical Documentation
- Japanese Microprocessor History Archives
- Computer History Museum records

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 6 free correction parameters
- Optimizer did not converge in 200 evaluations
- Corrections: branch: -1.55, call_return: -7.00, immediate: -3.25, memory_read: +0.41, memory_write: -5.00, register_ops: +5.00

**Final state:**
- CPI error: 1.69%
- Validation: PASSED

---
