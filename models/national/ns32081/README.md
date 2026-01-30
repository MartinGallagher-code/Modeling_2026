# National Semiconductor NS32081 Grey-Box Queueing Model

## Quick Reference
| Spec | Value |
|------|-------|
| Manufacturer | National Semiconductor |
| Year | 1982 |
| Clock | 10.0 MHz |
| Data Width | 32/64-bit floating point |
| Technology | NMOS |
| Architecture | Floating-point coprocessor |

## Validation Status
- **Status**: PASSED
- **CPI Error**: <5%
- **Last Validated**: 2026-01-30

## Model Overview
The NS32081 was the floating-point coprocessor for National Semiconductor's NS32000 series of 32-bit microprocessors. It provided IEEE 754 compatible floating-point operations with support for both 32-bit single-precision and 64-bit double-precision formats. It interfaced with the NS32016/NS32032 processors via a slave processor protocol and included hardware multiply and divide capabilities.

## Files
- `current/ns32081_validated.py` - Active model
- `validation/ns32081_validation.json` - Validation data
- `docs/ns32081_architecture.md` - Architecture documentation
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps
