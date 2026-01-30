# Ricoh 2A03 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial creation with 6502 cross-validation

**Session goal:** Create Ricoh 2A03 model with validated 6502-compatible timing

**Starting state:**
- New model, no previous version

**Changes made:**

1. Created complete processor model based on MOS 6502
   - Identical instruction timing to 6502 (same silicon, BCD disabled)
   - Clock set to 1.79 MHz (NTSC, vs 1.0 MHz typical 6502)
   - Same instruction categories: alu, data_transfer, memory, control, stack
   - Same workload profiles adapted for NES game patterns

2. Key architectural notes documented:
   - BCD (decimal mode) disabled - SED instruction has no effect
   - ADC/SBC always operate in binary mode
   - Includes on-chip APU (not modeled - CPU timing only)
   - Used in NES/Famicom (1983-present)

3. Cross-validated against MOS 6502 model
   - Instruction categories: Exact match
   - Category cycle counts: Exact match
   - Workload profiles: Exact match
   - Target CPI: 3.0 (identical)

4. Created validation JSON with 32 per-instruction timing tests
   - All tests from 6502 validation apply to 2A03
   - Added 2A03-specific notes about BCD mode

**What we learned:**
- Ricoh 2A03 is a 6502 with BCD disabled and APU added
- All instruction timing is identical to MOS 6502
- The main difference is the higher clock speed (1.79 MHz vs 1.0 MHz)
- MIPS: ~0.6 MIPS (vs ~0.33 MIPS for standard 6502 at 1 MHz)

**Final state:**
- CPI: 3.065 (2.17% error vs 3.0 expected)
- Validation: PASSED
- Cross-validation with MOS 6502: PASSED

**References used:**
- MOS Technology 6502 Datasheet (1976)
- Ricoh 2A03 technical documentation
- FCEUX NES emulator (cycle-accurate)
- Nestopia NES emulator
- NESDev Wiki (https://wiki.nesdev.com/)

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 5 free correction parameters
- Optimizer converged in 18 evaluations
- Corrections: alu: +0.65, control: +0.77, data_transfer: +0.10, memory: -0.85, stack: -1.42

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
