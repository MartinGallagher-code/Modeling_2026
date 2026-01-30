# Intel 8096 Grey-Box Queueing Model

## Quick Reference
| Spec | Value |
|------|-------|
| Manufacturer | Intel |
| Year | 1982 |
| Clock | 12.0 MHz |
| Data Width | 16-bit |
| Technology | CHMOS |
| Transistors | 120,000 |

## Validation Status
- **Status**: PASSED
- **CPI Error**: <5%
- **Last Validated**: 2026-01-30

## Model Overview
The Intel 8096 was a 16-bit microcontroller that dominated automotive applications from 1985 to 2005. It featured a register-based architecture (not accumulator-based) with a 232-byte register file, hardware multiply (16x16->32) and divide (32/16->16), on-chip PWM, A/D converter, high-speed I/O, serial port, timers, and watchdog. It was widely used in automotive engine control, fuel injection, and industrial control systems.

## Files
- `current/i8096_validated.py` - Active model
- `validation/i8096_validation.json` - Validation data
- `docs/i8096_architecture.md` - Architecture documentation
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps
