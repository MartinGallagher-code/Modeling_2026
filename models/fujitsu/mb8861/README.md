# Fujitsu MB8861 Grey-Box Queueing Model

## Quick Reference
| Spec | Value |
|------|-------|
| Manufacturer | Fujitsu |
| Year | 1977 |
| Clock | 1.0 MHz |
| Data Width | 8-bit |
| Technology | NMOS |
| Transistors | 4,100 |

## Validation Status
- **Status**: PASSED
- **CPI Error**: <5%
- **Last Validated**: 2026-01-30

## Model Overview
The Fujitsu MB8861 was a Motorola 6800-compatible clone manufactured by Fujitsu. It featured an 8-bit data bus, 16-bit address bus, two 8-bit accumulators (A, B), and a single index register (X). With identical instruction timing to the original 6800, it was used in Japanese arcade machines and early Japanese computers.

## Files
- `current/mb8861_validated.py` - Active model
- `validation/mb8861_validation.json` - Validation data
- `docs/mb8861_architecture.md` - Architecture documentation
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps
