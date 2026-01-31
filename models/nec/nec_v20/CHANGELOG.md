# NEC V20 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-28 - Initial model creation

**Session goal:** Create grey-box queueing model for the improved 8088 replacement

**Starting state:**
- No model existed

**Research findings:**
- NEC V20 was a pin-compatible 8088 replacement (1984)
- 10-20% faster than 8088 overall at same clock
- Hardware multiply/divide (3-4x faster than 8088's microcode)
- 63,000 transistors (vs 29,000 for 8088)
- 50% clock duty cycle (vs 33% for 8088)
- Dual internal 16-bit buses

**Changes made:**

1. Created model targeting CPI ~3.4 (15% faster than 8088's 4.0)
   - Cross-validated against existing i8088 model
   - Applied documented speedup factors

2. Added 6 instruction categories:
   - alu: 2 cycles (faster ADD/SUB than 8088)
   - data_transfer: 3 cycles
   - memory: 6 cycles (faster EA calculation)
   - control: 3 cycles
   - multiply: 6 cycles (weighted - hardware MUL is 3-4x faster)
   - divide: 10 cycles (weighted - ~3x faster than 8088)

3. Key V20 improvements modeled:
   - ADD reg,reg: 2 cycles (was 3 on 8088)
   - MUL 16-bit: 29-30 cycles (was 118-133 on 8088)
   - Faster effective address calculation

**What we learned:**
- V20's hardware multiply was the biggest single improvement
- The dual internal buses allowed more concurrent operations
- V20 also included 80186 instructions and 8080 emulation mode
- Some timing-sensitive software broke on V20 (ran too fast)

**Final state:**
- CPI: 3.55 (4.4% error vs target 3.4)
- Validation: PASSED
- Speedup vs 8088: ~1.13x (within expected 1.10-1.20x range)

**References used:**
- NEC V20/V30 User Manual
- Wikipedia: NEC V20
- CPU-World NEC V20 specifications
- TOPBENCH V20 vs 8088 benchmarks

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 6 free correction parameters
- Optimizer converged in 1 evaluations
- Corrections: all near zero (model already matched measurements)

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---

---

## [2026-01-31] - External benchmark data integration

**Session goal:** Replace synthetic CPI measurements with real published benchmark data

**Starting state:**
- CPI source: emulator/estimated (synthetic)
- Validation: based on self-referential data

**Changes made:**

1. Updated measured_cpi.json with externally-validated benchmark data
   - Source: published_benchmark
  - mips_rating: 0.4 MIPS @ 5.0MHz → CPI=12.50
   - Per-workload CPI derived using era-appropriate adjustment factors

2. Re-ran system identification with new measurement targets
   - Correction terms re-optimized via least-squares
   - CPI error: 32.00%

**What we learned:**
- External benchmark data provides honest validation targets
- Model error vs real benchmarks: 32.00%

**Final state:**
- CPI error: 32.00%
- Validation: NEEDS INVESTIGATION (against real benchmark data)
- Source: published_benchmark

**References used:**
- Netlib Dhrystone Database: https://www.netlib.org/performance/html/dhrystone.data.col0.html
- Wikipedia MIPS comparison: https://en.wikipedia.org/wiki/Instructions_per_second
- SPEC archives: https://www.spec.org/
