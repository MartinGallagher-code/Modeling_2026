# MOS 6507 Grey-Box Queueing Model

## Quick Reference
| Spec | Value |
|------|-------|
| Manufacturer | MOS Technology |
| Year | 1975 |
| Clock | 1.19 MHz |
| Data Width | 8-bit |
| Technology | NMOS |
| Transistors | 3,510 |

## Validation Status
- **Status**: PASSED
- **CPI Error**: <5%
- **Last Validated**: 2026-01-30

## Model Overview
The MOS 6507 was a cost-reduced version of the 6502 in a 28-pin package (reduced from 40 pins). It was electrically identical to the 6502 internally, with the same instruction set and timing, but exposed only 13 address lines (8KB address space) and omitted the RDY, SO, and NMI pins. It is best known as the CPU of the Atari 2600 (VCS) game console, running at 1.19 MHz.

## Files
- `current/mos6507_validated.py` - Active model
- `validation/mos6507_validation.json` - Validation data
- `docs/mos6507_architecture.md` - Architecture documentation
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps
