# TI TMS1000 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-28 - Initial model creation

**Session goal:** Create grey-box queueing model for the first commercial microcontroller

**Starting state:**
- No model existed

**Research findings:**
- TMS1000 was the first commercially available single-chip microcontroller (1974)
- All 43 base instructions execute in exactly 6 clock cycles (fixed timing)
- 4-bit data path with Harvard architecture
- Typical clock: 300 kHz (range 100-400 kHz)
- Performance: ~50 KIPS at 300 kHz

**Changes made:**

1. Created model with fixed 6-cycle instruction timing
   - All instruction categories set to 6 cycles
   - CPI is always 6.0 regardless of workload mix
   - This makes the model trivially accurate

2. Added 5 instruction categories:
   - alu: ALU operations @6 cycles
   - data_transfer: TAM/TMA transfers @6 cycles
   - memory: LDP/LDX operations @6 cycles
   - control: BR/CALL @6 cycles
   - io: TDO/SETR/RSTR @6 cycles

3. Added validation tests:
   - CPI exactly 6.0
   - IPS ~50,000 at 300 kHz
   - All workloads produce identical CPI

**What we learned:**
- TMS1000's fixed timing simplifies modeling significantly
- The LFSR-based program counter is unusual but doesn't affect timing
- Single-level stack severely limits recursion
- BCD arithmetic support made it ideal for calculators

**Final state:**
- CPI: 6.0 (0.0% error)
- Validation: PASSED
- 10/10 per-instruction timing tests passing

**References used:**
- TMS1000 Series Data Manual (December 1976)
- WikiChip TMS1000 article
- Wikipedia: Texas Instruments TMS1000

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 1 evaluations
- Corrections: all near zero (model already matched measurements)

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
