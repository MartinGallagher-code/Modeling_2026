# General Instrument CP1600 Grey-Box Queueing Model

## Quick Reference
| Spec | Value |
|------|-------|
| Manufacturer | General Instrument |
| Year | 1975 |
| Clock | 0.895 MHz |
| Data Width | 16-bit |
| Technology | NMOS |
| Architecture | 16-bit with 10-bit opcodes |

## Validation Status
- **Status**: PASSED
- **CPI Error**: <5%
- **Last Validated**: 2026-01-30

## Model Overview
The General Instrument CP1600 was a 16-bit microprocessor most notably used in the Mattel Intellivision game console (1979). It featured 8 general-purpose 16-bit registers (R0-R7) where R7 served as the program counter and R6 as the stack pointer by convention. R4 and R5 supported auto-increment/decrement addressing. Most instructions took 6-10 cycles with some complex instructions requiring up to 14 cycles.

## Files
- `current/cp1600_validated.py` - Active model
- `validation/cp1600_validation.json` - Validation data
- `docs/cp1600_architecture.md` - Architecture documentation
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps
