# Intel 4004 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-28 - Initial calibration

**Session goal:** Achieve <5% CPI prediction error

**Starting state:**
- CPI: uncalibrated (high error)
- Key issues: Model used wrong function signature or uncalibrated template

**Changes made:**

1. Rewrote model to use correct analyze() method
   - Replaced simulate() with analyze() returning AnalysisResult
   - Calibrated instruction cycle counts for target CPI
   - Result: Achieved <5% error

**What we learned:**
- The Intel 4004 (1971) was the world's first commercial microprocessor
- 4-bit architecture with 10um PMOS technology, only 2300 transistors
- Clock speed of 0.74 MHz, instructions take 8-16 cycles (1-2 machine cycles)
- Each machine cycle is 8 clock cycles, so effective CPI is very high

**Final state:**
- CPI: 10.6 (1.9% error vs expected 10.8)
- Validation: PASSED

---

## 2026-01-28 - Cross-validation with per-instruction timing tests

**Session goal:** Add comprehensive per-instruction timing tests and cross-validation with related processors

**Starting state:**
- CPI: 10.6 (1.9% error vs expected 10.8)
- Model validated but lacked detailed timing tests

**Changes made:**

1. Added 15 per-instruction timing tests to validation JSON
   - Documented opcodes and machine cycle counts for each instruction
   - Single-cycle (8 clocks): NOP, ADD, SUB, INC, LD, XCH, LDM, WRM, RDM, DAA
   - Two-cycle (16 clocks): JUN, JCN, FIM, JMS, ISZ

2. Added cross_validation section
   - Documented relationship with Intel 4040 (successor)
   - Added timing consistency rules for MCS-4 family
   - Documented architectural constraints (8-clock machine cycle at 740 kHz)

**What we learned:**
- The 4004 has a very regular timing model: all instructions are either 8 or 16 cycles
- The 10.8 us cycle time comes from 8 clock cycles at 740 kHz
- Two-cycle instructions need extra cycle for operand/address fetch

**Final state:**
- CPI: 10.6 (1.9% error) - unchanged, model already validated
- Cross-validation: Added relationship documentation with 4040
- Timing tests: 15 instructions documented with opcodes

**References used:**
- Intel 4004 datasheet (chipdb.org)
- WikiChip MCS-4 documentation

---
