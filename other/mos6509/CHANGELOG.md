# MOS 6509 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create MOS 6509 model based on MOS 6502

**Starting state:**
- No existing model

**Changes made:**

1. Created complete model based on MOS 6502:
   - Same instruction set and timing (6509 is 6502 with bank switching)
   - Instruction categories: alu, data_transfer, memory, control, stack
   - Target CPI: 3.0 (cross-validated from 6502)

2. Documented 6509-specific features:
   - Bank switching via $0000 (IndBank) and $0001 (ExecBank)
   - 20-bit address space (1 MB) with banking
   - Used in Commodore CBM-II (B and P series)
   - 1 MHz clock (same as 6502)

3. Added CBM-II-specific workload profile:
   - 'bank_heavy' for applications using multiple memory banks

4. Validation tests include:
   - CPI accuracy (target 3.0)
   - Workload weight sums
   - Cycle count ranges
   - IPC range
   - 6509-specific: banked address width (20 bits), clock (1.0 MHz)

**Final state:**
- CPI: 3.065 (2.17% error vs target 3.0)
- All validation tests passing
- Model consistent with MOS 6502 timing

**References used:**
- MOS Technology 6502 Datasheet (May 1976)
- MOS 6502 model (this project)
- Commodore CBM-II Technical Reference

---
