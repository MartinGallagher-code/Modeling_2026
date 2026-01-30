# MC14500B Model Changelog

This file contains the history of all work on this model.
**Append-only: Do not delete previous entries.**

---

## 2026-01-29 - Complete rewrite with correct timing

**Session goal:** Fix fundamentally incorrect model using actual Motorola handbook data

**Critical fix:**
- CPI corrected from 2.225 to **1.0** (all 16 instructions are single-cycle)
- Removed fake 4-stage pipeline model (MC14500B is combinational)
- Fixed bus_width from 8 to 1 (1-bit data path)
- Corrected JMP/RTN: they are output flags, not internal branches
- All timing tests now reference actual handbook pages
- Added real sources: Motorola Handbook (1977), Ken Shirriff reverse-engineering, WikiChip

**Changed:**
- `current/mc14500b_validated.py` - Complete rewrite with fixed 1-cycle model
- `mc14500b_model.json` - Fixed bus_width, timing categories, validation targets
- `validation/mc14500b_validation.json` - All 16 instructions verified, real sources
- `docs/mc14500b_architecture.md` - Correct architecture diagram and ISA table
- `HANDOFF.md` - Updated with correct performance data
- `README.md` - Updated with correct usage example

**Performance (corrected):**
- CPI = 1.0 (was incorrectly 2.225)
- IPS @ 1 MHz = 1,000,000 (was incorrectly ~450,000)
- Validation: 0% CPI error (trivially accurate)

---

## 2026-01-29 - Initial model draft and scaffolding (SUPERSEDED)

**Session goal:** Create full model package structure for MC14500B

**Added:**
- `current/mc14500b_validated.py` (draft validated-style model)
- `mc14500b_model.py` (queueing-based model with validation suite)
- `mc14500b_model.json` (config + timing categories)
- `validation/mc14500b_validation.json` (specs + timing tests)
- `docs/mc14500b_architecture.md` (architecture & modeling notes)
- `README.md`, `__init__.py`, `HANDOFF.md`

**Model summary:**
- Architecture: 1-bit industrial controller (1976)
- Categories: logic, io, branch, memory, control
- Typical CPI (draft): ~2.2 @ 1 MHz → ~450k IPS
- Bottleneck (typical): logic

**Notes:**
- Draft timing pending deeper datasheet review and corpus of ladder-logic examples
- Validation JSON includes placeholder tests for category timing coverage

**Next:**
- Tighten cycles and weights using Motorola handbook + app notes
- Add real instruction-level examples (e.g., RRL, I/O sense sequences)
- Expand validation targets with documented performance envelopes

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 4 free correction parameters
- Optimizer converged in 1 evaluations
- Corrections: all near zero (model already matched measurements)

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
