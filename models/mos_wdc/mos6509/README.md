# MOS 6509 Grey-Box Queueing Model

## Quick Reference
| Spec | Value |
|------|-------|
| Manufacturer | MOS Technology |
| Year | 1980 |
| Clock | 1.0 MHz |
| Data Width | 8-bit |
| Technology | NMOS |
| Transistors | 4,000 |

## Validation Status
- **Status**: PASSED
- **CPI Error**: <5%
- **Last Validated**: 2026-01-30

## Model Overview
The MOS 6509 was a 6502 variant with added bank switching capability. It extended the 6502's 16-bit address bus to a 20-bit address space (1 MB) via bank registers at addresses $0000 (IndBank) and $0001 (ExecBank). The core instruction timing was identical to the 6502. It was used in the Commodore CBM-II (B series and P series) computers.

## Files
- `current/mos6509_validated.py` - Active model
- `validation/mos6509_validation.json` - Validation data
- `docs/mos6509_architecture.md` - Architecture documentation
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps
