# Intel 4040 Model Changelog

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
- The Intel 4040 (1974) was an enhanced version of the 4004 with interrupt support
- 4-bit architecture with 10um PMOS technology, 3000 transistors
- Added halt instruction, interrupt handling, and expanded instruction set
- Same 0.74 MHz clock but more efficient instruction execution

**Final state:**
- CPI: 10.57 (0.7% error vs expected 10.5)
- Validation: PASSED

---

## 2026-01-28 - Cross-validation with per-instruction timing tests

**Session goal:** Add comprehensive per-instruction timing tests and cross-validation with related processors

**Starting state:**
- CPI: 10.57 (0.7% error vs expected 10.5)
- Model validated but lacked detailed timing tests

**Changes made:**

1. Added 15 per-instruction timing tests to validation JSON
   - Documented opcodes and machine cycle counts for each instruction
   - Single-cycle (8 clocks): NOP, ADD, SUB, INC, HLT, LD, XCH, LDM, RPL, WRM, RDM
   - Two-cycle (16 clocks): JUN, JCN, FIM, JMS

2. Added cross_validation section
   - Documented relationship with Intel 4004 (predecessor)
   - Added timing consistency rules for MCS-4 family
   - Documented new 4040 features: HLT, RPL (interrupt support), deeper stack

**What we learned:**
- The 4040 maintains 4004 timing compatibility (8/16 cycle pattern)
- New instructions like HLT and RPL follow the single-cycle pattern
- Stack depth increased from 3 levels to 7 levels

**Final state:**
- CPI: 10.57 (0.7% error) - unchanged, model already validated
- Cross-validation: Added relationship documentation with 4004
- Timing tests: 15 instructions documented with opcodes

**References used:**
- Intel 4040 datasheet (chipdb.org)
- WikiChip MCS-4 documentation

---
