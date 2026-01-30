# NEC uCOM-4 Grey-Box Queueing Model

## Quick Reference
| Spec | Value |
|------|-------|
| Manufacturer | NEC |
| Year | 1972 |
| Clock | 0.4 MHz |
| Data Width | 4-bit |
| Technology | PMOS |
| Transistors | 7,500 |

## Validation Status
- **Status**: PASSED
- **CPI Error**: <5%
- **Last Validated**: 2026-01-30

## Model Overview
The NEC uCOM-4 was NEC's first microcontroller and a competitor to the TI TMS1000. It featured a 4-bit data path with a parallel ALU and Harvard architecture. Most instructions executed in 6 clock cycles. It was used in calculators, watches, and consumer electronics as a Japanese alternative to American microcontrollers.

## Files
- `current/ucom4_validated.py` - Active model
- `validation/ucom4_validation.json` - Validation data
- `docs/ucom4_architecture.md` - Architecture documentation
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps
