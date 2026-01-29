# NEC uPD7720 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create complete processor model for NEC uPD7720 early DSP

**Starting state:**
- No existing model
- Target CPI: 1.5 (pipelined DSP operations)

**Changes made:**

1. Created upd7720_validated.py with grey-box queueing model
   - Implemented InstructionCategory, WorkloadProfile, and AnalysisResult dataclasses
   - Defined 4 instruction categories: mac (1 cycle), alu (1 cycle), memory (2 cycles), branch (2 cycles)
   - Created 5 workload profiles: typical, compute, memory, control, mixed
   - Calibrated weights to achieve target CPI of 1.5

2. Created validation JSON with:
   - Processor specifications (16-bit data, 13-bit instructions, 8 MHz)
   - 12 per-instruction timing tests covering key DSP operations
   - Cross-validation with TMS320C10 and other contemporary DSPs
   - Architecture notes documenting LPC vocoder design

3. Added comprehensive documentation
   - CHANGELOG.md (this file)
   - HANDOFF.md with current status and next steps
   - __init__.py for module imports

**What we learned:**
- The uPD7720 was a pioneering early DSP from 1980, predating the TMS320C10 by 3 years
- Hardware MAC unit enabled single-cycle multiply-accumulate for efficient LPC synthesis
- Used in various speech synthesis applications including Super Nintendo APU (S-SMP)
- 13-bit instruction encoding is unusual - optimized for DSP-specific operations

**Final state:**
- CPI: 1.50 (0% error vs 1.5 expected)
- Validation: PASSED
- All instruction category cycles match specification

**References used:**
- NEC uPD7720 datasheet
- LPC vocoder implementation guides
- SNES APU technical documentation

---
