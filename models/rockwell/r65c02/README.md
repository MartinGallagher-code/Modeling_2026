# Rockwell R65C02 Grey-Box Queueing Model

## Quick Reference
| Spec | Value |
|------|-------|
| Manufacturer | Rockwell International |
| Year | 1983 |
| Clock | 4.0 MHz |
| Data Width | 8-bit |
| Technology | CMOS |
| Transistors | 9,000 |

## Validation Status
- **Status**: PASSED
- **CPI Error**: <5%
- **Last Validated**: 2026-01-30

## Model Overview
The Rockwell R65C02 was a CMOS implementation of the 6502 compatible with the WDC 65C02 but with additional Rockwell-specific bit manipulation instructions (RMB, SMB, BBR, BBS). These bit test and manipulation instructions were particularly useful for embedded control applications. It offered lower power consumption than the NMOS 6502 and higher clock speeds up to 4 MHz. It was used in embedded systems, industrial controllers, and the Apple IIc.

## Files
- `current/r65c02_validated.py` - Active model
- `validation/r65c02_validation.json` - Validation data
- `docs/r65c02_architecture.md` - Architecture documentation
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps
