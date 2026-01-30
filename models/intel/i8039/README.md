# Intel 8035/8039 Grey-Box Queueing Model

## Quick Reference
| Spec | Value |
|------|-------|
| Manufacturer | Intel |
| Year | 1976 |
| Clock | 6.0 MHz |
| Data Width | 8-bit |
| Technology | NMOS |
| Transistors | 6,000 |

## Validation Status
- **Status**: PASSED
- **CPI Error**: <5%
- **Last Validated**: 2026-01-30

## Model Overview
The Intel 8035/8039 were ROM-less variants of the MCS-48 family of microcontrollers. The 8035 included 64 bytes of RAM with no internal ROM, while the 8039 had 128 bytes of RAM. They shared the same instruction set as the 8048, with most instructions executing in 1-2 cycles. External ROM was required for program storage, making them suitable for prototyping and systems requiring external program memory.

## Files
- `current/i8039_validated.py` - Active model
- `validation/i8039_validation.json` - Validation data
- `docs/i8039_architecture.md` - Architecture documentation
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps
