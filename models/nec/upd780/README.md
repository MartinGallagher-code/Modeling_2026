# NEC uPD780 Grey-Box Queueing Model

## Quick Reference
| Spec | Value |
|------|-------|
| Manufacturer | NEC |
| Year | 1976 |
| Clock | 2.5 MHz |
| Data Width | 8-bit |
| Technology | NMOS |
| Transistors | 8,500 |

## Validation Status
- **Status**: PASSED
- **CPI Error**: <5%
- **Last Validated**: 2026-01-30

## Model Overview
The NEC uPD780 was a Z80-compatible clone manufactured by NEC. It featured full Z80 instruction set compatibility including block transfer/search instructions (LDIR, CPIR), two register sets (main and alternate), and IX/IY index registers. It was used in the NEC PC-8001, PC-8801, and various Japanese computers.

## Files
- `current/upd780_validated.py` - Active model
- `validation/upd780_validation.json` - Validation data
- `docs/upd780_architecture.md` - Architecture documentation
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps
